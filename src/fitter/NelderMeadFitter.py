import logging

from numpy import mean, argsort, concatenate
from numpy.linalg import norm

from src import Face
from .ModelFitter import ModelFitter


class NelderMeadFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None, offset=1.,
                 initial_face=None, callback=None):
        super(NelderMeadFitter, self).__init__(image, dimensions, model,
                                               initial_face)

        self.__step = None
        self.__parameters = [None] * (self._dimensions)
        self.__errors = [None] * (self._dimensions)
        self.__normals = None
        self.__offset = offset

        self.__centroid = None
        self.__reflection = None
        self.reflection_error = None
        self.__expansion = None
        self.expansion_error = None
        self.__contraction = None
        self.contraction_error = None
        self.__end = None
        self.end_error = None

        self.__alpha = 1.
        self.__gamma = 2.
        self.__rho = .5
        self.__sigma = .5

    def start(self):
        self.__initiate_parameters()

    def __initiate_parameters(self):
        self.__step = 'start'
        initial_parameters = concatenate((
            self._initial_face.coefficients,
            [self._initial_face.ambient_light],
            self._initial_face.directed_light
        ))
        for i in range(len(self.__parameters)):
            logging.debug('Initial step %d of %d', i, self._dimensions)
            # self.__parameters[i] = randn(self._dimensions) * 1
            # self.__parameters[i] = zeros(self._dimensions)
            # self.__parameters[i][:i] = self.__offset
            self.__parameters[i] = initial_parameters.copy()
            self.__parameters[i][:i] += self.__offset
            self.request_face(Face.from_array(self.__parameters[i]), i)
        # self.__end = ones(self._dimensions)
        # self.__end = randn(self._dimensions)
        self.__end = initial_parameters + self.__offset
        self.request_face(Face.from_array(self.__end), self._dimensions)

    def receive_image(self, image, index=None):
        error = self.get_image_deviation(image)
        logging.debug('Received image for step %d with error %f',
                      self.__step, error)

        if self.__step in ['reflection', 'expansion', 'contraction']:
            setattr(self, self.__step + '_error', error)
            getattr(self, 'calculate_' + getattr(self, self.__step)())()

        elif self.__step == 'shrink' and index == self._dimensions:
            logging.debug('%d items left',
                          sum(1 if e is None else 0 for e in self.__errors))
            self.end_error = error
            if None not in self.__errors:
                self.__sort_parameters()
                getattr(self, 'calculate_' + getattr(self, self.__step)())()
        elif self.__step == 'shrink':
            logging.debug('%d items left',
                          sum(1 if e is None else 0 for e in self.__errors))
            self.__errors[index] = error
            if None not in self.__errors and self.end_error is not None:
                self.__sort_parameters()
                getattr(self, 'calculate_' + getattr(self, self.__step)())()

        elif self.__step == 'start' and index == self._dimensions:
            self.end_error = error
            if None not in self.__errors:
                logging.debug('Started reflection')
                self.__sort_parameters()
                self.calculate_reflection()
            else:
                logging.debug(
                    '%d items left',
                    sum(1 if e is None else 0 for e in self.__errors))
        elif self.__step == 'start':
            self.__errors[index] = error
            if None not in self.__errors and self.end_error is not None:
                logging.debug('Started reflection')
                self.__sort_parameters()
                self.calculate_reflection()
            elif None in self.__errors:
                logging.debug(
                    '%d items left',
                    sum(1 if e is None else 0 for e in self.__errors))
            else:
                logging.debug('One item left')

    def __sort_parameters(self):
        indices = argsort(self.__errors + [self.end_error])
        parameters = []
        errors = []

        for i in indices[:-1]:
            if i == self._dimensions:
                parameters.append(self.__end)
                errors.append(self.end_error)
            else:
                parameters.append(self.__parameters[i])
                errors.append(self.__errors[i])

        if indices[-1] != self._dimensions:
            self.end_error = self.__errors[indices[-1]]
            self.__end = self.__parameters[indices[-1]]

        self.__parameters = parameters
        self.__errors = errors

    def calculate_centroid(self):
        self.__centroid = mean(self.__parameters, axis=0)

    def calculate_reflection(self):
        self.__step = 'reflection'
        self.calculate_centroid()
        self.__reflection = self.__centroid + self.__alpha * \
            (self.__centroid - self.__end)
        self.request_face(Face.from_array(self.__reflection))

    def reflection(self):
        self.__sort_parameters()
        if self.__finished():
            return 'finish'
        if self.reflection_error < self.__errors[0]:
            return 'expansion'
        elif self.reflection_error >= self.__errors[-1]:
            return 'contraction'
        else:
            logging.debug(
                'R, E1, En: %f, %f, %f',
                self.reflection_error, self.__errors[0], self.__errors[-1])
            self.__end = self.__reflection
            self.end_error = self.reflection_error
            return 'reflection'

    def calculate_expansion(self):
        self.__step = 'expansion'
        self.__expansion = self.__centroid + self.__gamma * \
            (self.__reflection - self.__centroid)
        self.request_face(Face.from_array(self.__expansion))

    def expansion(self):
        if self.expansion_error < self.reflection_error:
            self.__end = self.__expansion
            self.end_error = self.expansion_error
        else:
            self.__end = self.__reflection
            self.end_error = self.reflection_error
        return 'reflection'

    def calculate_contraction(self):
        self.__step = 'contraction'
        self.__contraction = self.__centroid + self.__rho * \
            (self.__parameters[-1] - self.__centroid)
        self.request_face(Face.from_array(self.__contraction))

    def contraction(self):
        if self.contraction_error < self.end_error:
            self.__end = self.__contraction
            self.end_error = self.contraction_error
            return 'reflection'
        return 'shrink'

    def calculate_shrink(self):
        self.__step = 'shrink'
        self.__parameters[1:] = self.__parameters[0] + self.__sigma * \
            (self.__parameters[1:] - self.__parameters[0])
        self.__errors[1:] = [None] * (len(self.__errors) - 1)

        self.__end = self.__parameters[0] + self.__sigma * \
            (self.__end - self.__parameters[0])
        self.end_error = None

        for i in range(1, self._dimensions):
            self.request_face(Face.from_array(self.__parameters[i]), i)
        self.request_face(Face.from_array(self.__end), self._dimensions)

    def shrink(self):
        if self.__finished():
            return 'finish'
        else:
            return 'reflection'

    def calculate_finish(self):
        self.__step = 'finish'
        logging.debug(self.__parameters[0])
        logging.debug(self.__errors[0])

    def __finished(self):
        s = 0.
        for i in range(1, len(self.__parameters)):
            s += norm(self.__parameters[i] - self.__parameters[i-1])
        logging.debug('Perimeter is %f, error is %f', s, self.__errors[0])
        return s < .2
