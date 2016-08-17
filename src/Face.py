
from numpy import array, zeros, concatenate

ERROR_TEXT = {
    'VERTICES_SIZE': "Size of vertices array should be a multiple of three, "
                     "but {} provided",
    'TRIANGLES_SHAPE': "Need array of triangles (x, 3), "
                       "but array with shape {} provided",
    'TRIANGLES_VERTICES': "Each triangle should contain 3 vertices, "
                          "but {} provided",
    'LIGHT_DIRECTION': "Light should be represented by 3D vector, "
                       "but array of shape {} provided"
}


class Face:

    __triangles = None
    __triangles_flattened = None
    __triangles_c = None

    def __init__(self, ambient_light=0, directed_light=None,
                 coefficients=None):
        """Create new Face."""
        self.__directed_light = None
        self.__ambient_light = None

        self.ambient_light = ambient_light

        if directed_light is None:
            self.directed_light = zeros(3, dtype='f')
        else:
            self.directed_light = directed_light

        if coefficients is None:
            self.__coefficients = array([], dtype='f')
        else:
            self.__coefficients = coefficients

    @property
    def directed_light(self):
        return self.__directed_light

    @directed_light.setter
    def directed_light(self, directed_light):
        directed_light = array(directed_light)
        if directed_light.shape != (3,):
            raise ValueError(ERROR_TEXT['LIGHT_DIRECTION']
                             .format(directed_light.shape))
        self.__directed_light = directed_light

    @property
    def ambient_light(self):
        return self.__ambient_light

    @ambient_light.setter
    def ambient_light(self, ambient_light):
        self.__ambient_light = ambient_light

    @property
    def light(self):
        return concatenate((self.directed_light, [self.ambient_light]))

    @property
    def coefficients(self):
        return self.__coefficients

    @staticmethod
    def set_triangles(triangles=None, triangles_c=None):
        """Sets indices of vertices connected in triangles.

        Sets both NumPy and C arrays of triangles.
        """
        if triangles is not None:
            if len(triangles.shape) != 2:
                raise ValueError(ERROR_TEXT['TRIANGLES_SHAPE']
                                 .format(triangles.shape))
            elif triangles.shape[1] != 3:
                raise ValueError(ERROR_TEXT['TRIANGLES_VERTICES']
                                 .format(triangles.shape[1]))
            Face.__triangles = triangles
            Face.__triangles_flattened = triangles.flatten()
        if triangles_c is not None:
            Face.__triangles_c = triangles_c

    @staticmethod
    def from_array(parameters):
        coefficients = parameters[:-4]
        ambient_light = parameters[-4]
        directed_light = parameters[-3:]
        return Face(coefficients=coefficients,
                    directed_light=directed_light,
                    ambient_light=ambient_light)
