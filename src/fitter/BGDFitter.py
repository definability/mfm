from PIL import Image
from numpy import zeros, nonzero

from .ModelFitter import ModelFitter


class BGDFitter(ModelFitter):
    """Batch gradient descent."""
    def __init__(self, image, dimensions=199, model=None,
                 dx=.1, step=100., max_loops=10, callback=None,
                 initial=None, initial_face=None):

        self.__dx = dx
        self.__step = step
        self.__coefficients = None
        self.__current_step = 0
        self.__callback = callback

        self.__derivatives = None
        self.__left_derivatives = None
        self.__right_derivatives = None

        self.__loop = 0
        self.__max_loops = max_loops

        super(BGDFitter, self).__init__(image, dimensions, model, initial,
                                        initial_face)

    def start(self):
        self.__coefficients = self._initial.copy()

        self.__derivatives = zeros(self._dimensions, dtype='f')
        self.__left_derivatives = zeros(self._dimensions, dtype='f')
        self.__right_derivatives = zeros(self._dimensions, dtype='f')

        self.__next_iteration()

    def receive_normals(self, normals, index=None):
        if index == 'start_iteration':
            light = self.estimate_light(normals)
            shadows = normals.dot(light)
            # print('{:0>3}: Error is {}'.format(
            #     self.__loop, self.get_image_deviation(shadows, normals)))
            index = 'start'
            if self.__loop >= self.__max_loops:
                self.__finish(normals, shadows)
                return
        if index == 'start' and self.__current_step >= self._dimensions - 1:
            self.__next_iteration()
            return
        elif index == 'start':
            self.__current_step += 1

        self.__get_derivative(self.__current_step, index, normals)

    def __next_iteration(self):
        self.__loop += 1
        self.__current_step = -1
        self.__coefficients -= self.__step * self.__derivatives
        # print(self.__derivatives)
        # print(self.__coefficients)
        self.request_normals(self.__coefficients, 'start_iteration')

    def __get_derivative(self, param, step, normals):
        if step == 'start':
            light = self.estimate_light(normals)
            shadows = normals.dot(light)
            self.__derivatives[param] = self.get_image_deviation(shadows,
                                                                 normals)
            value = self.__coefficients[param] + self.__dx
            self.request_normals((param, value), 'right_derivative')
        elif 'derivative' in step:
            # print('.' if param % 10 else '*', end='', flush=True)
            light = self.estimate_light(normals)
            shadows = normals.dot(light)

            value = self.__coefficients[param]

            if 'right' in step:
                value -= self.__dx
                action = 'left_derivative'
                self.__right_derivatives[param] = self.__derivative(
                    self.__derivatives[param],
                    self.get_image_deviation(shadows, normals))
            elif 'left' in step:
                action = 'start'
                self.__left_derivatives[param] = self.__derivative(
                    self.get_image_deviation(shadows, normals),
                    self.__derivatives[param])
                self.__derivatives[param] = (
                    0.5 * (self.__left_derivatives[param]
                           + self.__right_derivatives[param]))

            self.request_normals((param, value), action)

    def __derivative(self, y0, y1):
        return (y1 - y0) / self.__dx

    def __finish(self, normals, shadows):
        img = shadows
        img[normals[:, 3] == 0.] = 1.
        img = img[::-1]
        image = Image.new('L', (500, 500))
        image.putdata((img*255).astype('i'))
        image.save('img.png'.format(self.__loop))
        image.close()
        if self.__callback is not None:
            self.__callback(self.__coefficients)
        # print('Finished')
