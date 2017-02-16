from numpy import linspace, concatenate

from src import Face
from .ModelFitter import ModelFitter


class CoordinateDescentFitter(ModelFitter):
    """Fitter which uses coordinate descent algorithm."""
    def __init__(self, image, dimensions=199, model=None,
                 max_loops=1, steps=None, components=None,
                 initial_face=None, callback=None):
        super(CoordinateDescentFitter, self).__init__(image, dimensions, model,
                                                      initial_face)
        self.__max_loops = max_loops
        self.__steps = steps
        if components is None:
            components = list(range(len(steps)))
        self.__components = components
        for i, component in enumerate(components):
            if component >= self._dimensions - Face.NON_PCS_COUNT:
                components[i] -= self._dimensions

    def start(self):
        parameters = self._initial_face.as_array.copy()
        for _ in range(self.__max_loops):
            parameters = self.__iteration(parameters)
        self.finish(Face.from_array(parameters))

    def __iteration(self, parameters):
        for component, steps_count in zip(self.__components, self.__steps):
            start, finish = self.__get_bounds(component)
            values = self.__get_values(start, finish, steps_count,
                                       parameters[component])
            parameters[component] = self.__find_best_value(values, parameters,
                                                           component)
        return parameters

    def __get_bounds(self, component):
        if component >= 0:
            start, finish = -3, 3
        elif (Face.LIGHT_COMPONENTS_START <= component
              < Face.LIGHT_COMPONENTS_END):
            start, finish = -1, 1
        elif (Face.DIRECTION_COMPONENTS_START <= component
              < Face.DIRECTION_COMPONENTS_END - 1):
            start, finish = -1, 1
        elif component == Face.DIRECTION_COMPONENTS_END - 1:
            start, finish = 0.5, 2
        elif (Face.SCALE_COMPONENTS_START <= component
              < Face.SCALE_COMPONENTS_END):
            start, finish = 0.5, 2
        else:
            assert False, 'Unknown component {}'.format(component)
        return start, finish

    def __get_values(self, start, finish, steps_count, initial_value):
        values = linspace(start, finish, steps_count + 1 + steps_count % 2,
                          dtype='f')
        if initial_value not in values:
            values = concatenate((values, [initial_value]))
            values.sort()
        return values

    def __find_best_value(self, values, parameters, component):
        current = parameters.copy()
        best_value = (values[0], float('inf'))
        for value in values:
            current[component] = value
            deviation = self.get_face_deviation(current)
            if deviation < best_value[1]:
                best_value = value, deviation
        if best_value[0] != values[-1]:
            current[value] = best_value[0]
            self.get_face(current)
        return value
