from numpy import ones, zeros

from src import Face
from .ModelFitter import ModelFitter


class BruteForceFitter(ModelFitter):
    def __init__(self, image, dimensions=199, model=None, steps=None,
                 levels=None, offsets=None, scales=None,
                 initial_face=None, callback=None):
        """
        All parameters are normalized to [0; 1] by default and divided by
        `steps` chunks.

        Corresponding parameter `offsets` added to this interval,
        then `scales` multiplied.

        Final formula for current `step`:
        ```
        v = (step / steps)
        result = scale * (v + offset)
        ```

        You can chose `scale` and `offset` parameters to `0` to bypass some
        parameter and leave it on zero value.

        Sequence `levels` contains indices of parameters
        which should be fitted.
        """
        super(BruteForceFitter, self).__init__(
            image, dimensions, model, initial_face, callback)

        if steps is None:
            self.__steps = ones(dimensions, dtype='i')
        else:
            self.__steps = steps

        if offsets is None:
            self.__offsets = zeros(dimensions, dtype='f')
        else:
            self.__offsets = offsets

        if scales is None:
            self.__scales = ones(dimensions, dtype='f')
        else:
            self.__scales = scales

        self.__current_step = None
        self.__parameters = zeros(dimensions, dtype='f')

        self.__errors = None
        self.__values = None

        self.__loop = 0
        self.__levels = levels
        self.__indices = []
        self.__directions = []
        self.__face = None


    def start(self):
        self.__loop = 0
        self.__face = self._initial_face
        self.__parameters = self._initial_face.as_array

        self.request_face(self.__face, 'init')

        self.__errors = {}
        self.__generate_errors()
        self.__indices = [0] * len(self.__levels)
        self.__directions = [1] * len(self.__levels)

        self.__parameters[self.__levels] = [
            self.__get_value(i, self.__indices[i])
            for i in range(len(self.__levels))]

        change_on = 0
        while change_on != -1:
            self.__errors[tuple(self.__indices)] = self.__get_parameter(
                change_on=change_on)
            change_on = self.__inc_index()

        result = self.__convert_parameters()

        parameters = self._initial_face.as_array
        parameters[self.__levels] = result[-1][0]

        face = Face.from_array(parameters)
        self.get_face(face)

        self.finish(face)

    def __generate_errors(self, current_level=0, tail=None):
        if tail is None:
            tail = []
        if current_level == len(self.__levels) - 1:
            for value in range(self.__steps[current_level]):
                self.__errors[tuple(tail + [value])] = None
            return
        else:
            for value in range(self.__steps[current_level]):
                self.__generate_errors(current_level + 1, tail + [value])

    def __get_value(self, level, item):
        normalized_value = item / self.__steps[level] + self.__offsets[level]
        return self.__scales[level] * normalized_value

    def __get_values(self, parameters):
        return [self.__get_value(i, p) for i, p in enumerate(parameters)]

    def __get_parameter(self, change_on=0):
        value = self.__get_value(change_on, self.__indices[change_on])
        self.__parameters[self.__levels[change_on]] = value
        self.__face = Face.from_array(self.__parameters)
        return self.get_face_deviation(self.__face)

    def __inc_index(self, level=0):
        self.__indices[level] += self.__directions[level]
        if self.__indices[level] >= 0 \
                and self.__indices[level] <= self.__steps[level]:
            return level
        elif level == len(self.__levels) - 1:
            return -1
        self.__directions[level] = - self.__directions[level]
        self.__indices[level] += self.__directions[level]
        return self.__inc_index(level + 1)

    def __convert_parameters(self):
        sorted_parameters = sorted(self.__errors.items(), key=lambda x: -x[1])
        return [(tuple(self.__get_values(p)), e) for p, e in sorted_parameters]

    def finish(self, face):
        return super(BruteForceFitter, self).finish(face)
