from PIL import Image
from numpy import ones, zeros, linspace, argmin, nonzero, column_stack
from numpy.random import rand, randint

from .ModelFitter import ModelFitter

class GibbsSamplerFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None, steps=None,
                 max_loops=1):
        self.__steps = ones(dimensions, dtype='i') if steps is None else steps
        self.__current_step = None
        self.__parameters = zeros(dimensions, dtype='f')

        self.__errors = None
        self.__values = None
        self.__max_loops = max_loops

        super(GibbsSamplerFitter, self).__init__(image, dimensions, model)

    def start(self):
        # self.__get_parameter(randint(0, self._dimensions))
        self.__loop = 0
        self.__get_parameter(0)

    def __get_parameter(self, i):
        self.__current_step = i

        if self.__steps[i] % 2 == 0:
            self.__values = linspace(-4, 4, self.__steps[i] + 1, dtype='f')
        else:
            self.__values = linspace(-4, 4, self.__steps[i] + 2, dtype='f')

        self.__errors = [None] * self.__values.size
        for i, value in enumerate(self.__values):
            self.__values[i] = value
            parameters = self.__parameters.copy()
            parameters[self.__current_step] = value
            self.request_normals(parameters, i)

    def receive_normals(self, normals, index=None):
        light = self.estimate_light(normals)
        shadows = normals.dot(light)
        # shadows[nonzero(normals)[0]] = abs(rand(nonzero(normals)[0].size))

        if index is None:
            self.finish(normals, shadows)
            return

        self.__errors[index] = self.get_image_deviation(shadows, normals)

        if None in self.__errors:
            return

        best_index = argmin(self.__errors)
        self.__parameters[self.__current_step] = self.__values[best_index]
        print('{}.{}: Error of the best is {}'.format(
            self.__loop, self.__current_step, self.__errors[best_index]))

        if self.__current_step + 1 == self._dimensions and self.__loop == 2:
            self.request_normals(self.__parameters)
            return
        elif self.__current_step + 1 == self._dimensions:
            self.__current_step = -1
            self.__loop += 1

        self.__get_parameter(self.__current_step + 1)

    def finish(self, normals, shadows):
        img = shadows[::-1]
        alpha = zeros(len(normals[:, 3]))
        alpha[nonzero(normals[:, 3])[0]] = 1.
        data = (column_stack((
                img, img, img,
                alpha
                )) * 255).astype('i')
        image = Image.new('L', (500, 500))
        image.putdata((img*255).astype('i'))
        image.save('img.png')
        print('Finished')
