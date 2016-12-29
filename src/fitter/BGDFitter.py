import logging

from PIL import Image
from numpy import zeros

from src import Face
from .ModelFitter import ModelFitter


class BGDFitter(ModelFitter):
    """Batch gradient descent."""
    def __init__(self, image, dimensions=199, model=None,
                 dx=.1, step=100., max_loops=10, callback=None,
                 initial_face=None, light_dx=.1):
        super(BGDFitter, self).__init__(image, dimensions, model, initial_face)

        self.__dx = dx
        self.__light_dx = light_dx
        self.__step = step
        self.__face = None
        self.__current_step = -5
        self.__callback = callback

        self.__derivatives = None
        self.__left_derivatives = None
        self.__right_derivatives = None

        self.__loop = 0
        self.__max_loops = max_loops

    def start(self):
        self.__face = self._initial_face

        derivatives_size = self._dimensions
        self.__derivatives = zeros(derivatives_size, dtype='f')
        self.__left_derivatives = zeros(derivatives_size, dtype='f')
        self.__right_derivatives = zeros(derivatives_size, dtype='f')

        self.__next_iteration()

    def receive_image(self, image, index=None):
        if index != 'start':
            self.__get_derivative(self.__current_step, index, image)
        elif self.__loop >= self.__max_loops:
            self.__finish(image)
        elif self.__current_step >= self._dimensions - 1:
            self.__next_iteration()
        else:
            self.__current_step += 1

    def __next_iteration(self):
        self.__loop += 1
        self.__current_step = -5
        coefficients = (
            self.__face.coefficients
            - self.__step * self.__derivatives[:-Face.NON_PCS_COUNT])
        directed_light = (
            self.__face.directed_light
            - self.__step * self.__derivatives[Face.LIGHT_COMPONENTS_SLICE]
            / 50)
        self.__face = Face(coefficients=coefficients,
                           directed_light=directed_light)
        logging.debug('Derivatives: %s', self.__derivatives)
        self.request_face(self.__face, 'start')

    def __get_derivative(self, param, step, image):
        if step == 'start':
            self.__derivatives[param] = self.get_image_deviation(image)
            face = self.__derivative_face(param, self.__dx)
            self.request_face(face, 'right_derivative')
        elif 'derivative' in step:
            self.__calculate_derivative(param, step, image)

    def __calculate_derivative(self, param, step, image):
        face = self.__face
        dx = self.__dx if param >= 0 else self.__light_dx

        if 'right' in step:
            face = self.__derivative_face(param, -self.__dx)

            action = 'left_derivative'
            self.__right_derivatives[param] = self.__derivative(
                self.__derivatives[param],
                self.get_image_deviation(image),
                dx)
        elif 'left' in step:
            action = 'start'
            self.__left_derivatives[param] = self.__derivative(
                self.get_image_deviation(image),
                self.__derivatives[param],
                dx)
            self.__derivatives[param] = (
                0.5 * (self.__left_derivatives[param]
                       + self.__right_derivatives[param]))

        self.request_face(face, action)

    def __derivative_face(self, param, dx):
        params = self.__face.as_array
        if param >= 0:
            params[param] += dx
        else:
            params[param] += self.__light_dx

        return Face.from_array(params)

    def __derivative(self, y0, y1, dx):
        return (y1 - y0) / dx

    def __finish(self, shadows):
        img = shadows
        img[shadows[:, 3] == 0.] = 1.
        img = img[::-1]
        image = Image.new('L', (500, 500))
        image.putdata((img*255).astype('i'))
        image.save('img.png'.format(self.__loop))
        image.close()
        if self.__callback is not None:
            self.__callback(self.__face)
        logging.debug('Finished')
