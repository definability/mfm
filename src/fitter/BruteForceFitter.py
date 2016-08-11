from numpy import ones, zeros

from .ModelFitter import ModelFitter
from src import Face


class BruteForceFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None, steps=None,
                 max_level=3):
        dimensions += 4
        self.__steps = ones(dimensions, dtype='i') if steps is None else steps
        self.__current_step = None
        self.__parameters = zeros(dimensions, dtype='f')

        self.__errors = None
        self.__values = None

        self.__loop = 0
        self.__max_level = max_level
        self.__indices = []
        self.__directions = []
        self.__face = None

        super(BruteForceFitter, self).__init__(image, dimensions, model)

    def start(self):
        self.__loop = 0
        self.__parameters = zeros(self._dimensions, dtype='f')
        self.__face = Face.from_array(self.__parameters)
        self.request_face(self.__face, 'init')

        self.__errors = {}
        self.__generate_errors()
        self.__indices = [0] * self.__max_level
        self.__directions = [1] * self.__max_level

        self.__parameters = ([self.__get_value(i, self.__indices[i])
                             for i in range(self.__max_level)]
                             + [0] * (self._dimensions - self.__max_level))

        self.__get_parameter()

    def __generate_errors(self, current_level=0, tail=None):
        if tail is None:
            tail = []
        if current_level == self.__max_level - 1:
            for value in range(self.__steps[current_level]):
                self.__errors[tuple(tail + [value])] = None
            return
        else:
            for value in range(self.__steps[current_level]):
                self.__generate_errors(current_level + 1, tail + [value])

    def __get_value(self, level, item):
        return 6. * (item - self.__steps[level] * .5) / self.__steps[level]

    def __get_values(self, parameters):
        return [self.__get_value(i, p) for i, p in enumerate(parameters)]

    def __get_parameter(self, index=None, change_on=0):
        value = self.__get_value(change_on, self.__indices[change_on])
        self.__parameters[change_on] = value
        self.__face = Face.from_array(self.__parameters)
        self.request_face(self.__face, index)

    def __inc_index(self, level=0):
        self.__indices[level] += self.__directions[level]
        if self.__indices[level] >= 0 \
                and self.__indices[level] <= self.__steps[level]:
            return level
        elif level == self.__max_level - 1:
            return -1
        self.__directions[level] = - self.__directions[level]
        self.__indices[level] += self.__directions[level]
        return self.__inc_index(level + 1)

    def receive_image(self, image, index=None):
        if index == 'init':
            return
        elif index == 'finish':
            self.finish()
            return
        shadows = image

        self.__errors[tuple(self.__indices)] = self.get_image_deviation(shadows)

        change_on = self.__inc_index()
        if change_on == -1:
            result = self.__convert_parameters()
            self.__face = Face.from_array(result[-1][0])
            self.request_face(self.__face, 'finish')
            return

        self.__get_parameter(change_on=change_on)

    def __convert_parameters(self):
        sorted_parameters = sorted(self.__errors.items(), key=lambda x: -x[1])
        return [(tuple(self.__get_values(p)), e) for p, e in sorted_parameters]

    def finish(self):
        return
