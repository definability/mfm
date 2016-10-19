from math import pi
from decimal import Decimal

from numpy import array, unique, zeros, std, log, mean, isnan
from numpy.random import randn

from src import Face
from .ModelFitter import ModelFitter


class MonteCarloFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None, initial_face=None,
                 estimating_parameters=None, iterating_parameters=None,
                 steps=100, callback=None):
        """
        Keyword arguments:
        - estimating_parameters Parameters to estimate.
        - iterating_parameters  Parameters to integrate by
                                in addition to parameters to estimate.
        """
        assert len(estimating_parameters) > 0
        if iterating_parameters is None:
            iterating_parameters = list(range(dimensions))

        dimensions += 4
        image = array(image) / 16

        self.__iterating_parameters = unique(
            estimating_parameters + iterating_parameters)
        self.__estimating_parameters = array(estimating_parameters)

        self.__parameters = None
        self.__differences = None
        self.__image = image
        self.__values = []
        self.__steps = steps

        super(MonteCarloFitter, self).__init__(image, dimensions - 4, model,
                                               initial_face, callback)
        self._dimensions += 4

    def start(self):
        self.__parameters = []
        self.__differences = []

        for parameter in range(self.__steps):
            self.request_face(self.__generate_face_parameters(), parameter)

    def receive_image(self, image, index=None):
        indices = (image[:, 0] != image[:, 2])

        difference = (self.__image - image[:, 0])[indices].flatten()
        variance = std(difference)**2

        power = - (
            self.__image.size
            * ((difference**2).sum() / (2*variance)) / difference.size
            - 0.5 * self.__image.size * log(2 * pi * variance)
            )
        if difference.size == 0 or variance == 0 or isnan(power):
            # print('Zero Parameters:', self.__parameters[index])
            self.request_face(self.__generate_face_parameters(), index)
            return
        self.__differences[index] = power
        if None not in self.__differences:
            self.__calculate_result()

        # if self.__differences.count(None) % 1000 == 0 \\
        #       and self.__differences.count(None) < len(self.__differences):
        #     params = [p for d, p in zip(self.__differences, self.__parameters) if d is not None]
        #     tmp = [(d, p) for d, p in zip(
        #         self.__get_probabilities(self.__differences), params)]
        #     self.__get_iterations_count(tmp)

    def __calculate_result(self):
        """Get weighted sum of achieved parameters.

        Normalize probabilities as their sum should be 1.
        Then get sum of parameters got during iterations
        multiplied by corresponding probabilities.

        Form parameters of final face and finish the fitting procedure.
        """
        max_difference = max(self.__differences)
        normalized_differences = array(self.__differences) - float(
            sum(Decimal(diff - max_difference).exp()
                for diff in self.__differences).ln())
        params = [
            sum(
                Decimal(float(p[i]))*Decimal(diff).exp()
                for diff, p in zip(normalized_differences, self.__parameters))
            for i in self.__estimating_parameters]
        face = self._initial_face
        parameters = zeros(self._dimensions, dtype='f')
        parameters[-4] = face.ambient_light
        parameters[-3:] = face.directed_light
        parameters[:-4] = face.coefficients
        parameters[self.__estimating_parameters] = params
        self.finish(face)

    def __get_iterations_count(self, values):
        """Estimate number of iterations.

        Calculate how much iterations needed with current variance
        to be 99% sure that relative error is not greater than 0.1.
        """
        average = sum(p * Decimal(float(v[0])) for p, v in values)
        variance = (sum(p * (Decimal(float(v[0]))**2) for p, v in values)
                    - mean**2)

        z = Decimal('2.575')**2
        epsilon = Decimal('0.01')**2

        return (z * variance / epsilon) / average

    def __get_probabilities(self, differences):
        """Get normalized probabilities."""
        normalizator = sum(Decimal(d).exp()
                           for d in differences if d is not None).ln()
        return [(Decimal(d) - normalizator).exp()
                for d in differences if d is not None]

    def __generate_face_parameters(self):
        """Generate random face.

        Based on needed parameters to iterate by and initial Face.
        """
        face = self._initial_face
        parameters = zeros(self._dimensions, dtype='f')
        parameters[-4] = face.ambient_light
        parameters[-3:] = face.directed_light
        parameters[:-4] = face.coefficients
        parameters[self.__iterating_parameters] = randn(
            len(self.__iterating_parameters))
        self.__parameters.append(parameters)
        self.__differences.append(None)
        self.__values.append(None)
        return Face.from_array(parameters)
