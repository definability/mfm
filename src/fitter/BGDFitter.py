import logging

from numpy import ones, zeros, array, save
from scipy.optimize import minimize, differential_evolution

from src import Face
from .ModelFitter import ModelFitter


class BGDFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None,
                 dx=.1, step=100., max_loops=10, callback=None,
                 initial_face=None, light_dx=.1):
        """Batch gradient descent."""
        super(BGDFitter, self).__init__(
            image, dimensions, model, initial_face, callback)
        self.__face = None
        self.__parameters = None
        self.__dx = dx
        self.__step = step
        self.__max_loops = max_loops

    def start(self):
        face = self._initial_face.as_array

        for _ in range(self.__max_loops):
            derivatives = self.__get_derivatives(face)
            face += derivatives * self.__step

        self.finish(Face.from_array(face))

    def __get_derivatives(self, face):
        return array([self.__get_derivative(face, i)
                      for i in range(self._dimensions)], 'f')

    def __get_derivative(self, face, i):
        k = 1
        dx = self.__dx
        if i >= self._dimensions - Face.NON_PCS_COUNT:
            k = .05
            dx /= 5
            return 0
        value = face[i]
        face[i] = value - dx
        left_value = self.get_face_deviation(face)
        face[i] = value + dx
        right_value = self.get_face_deviation(face)
        face[i] = value

        return k * (right_value - left_value) / (2 * self.__dx)

    def finish(self, face):
        return super(BGDFitter, self).finish(face)
