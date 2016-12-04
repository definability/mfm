
from numpy import array, zeros, concatenate, sin, cos

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
        """Get directed light vector."""
        return self.__directed_light

    @property
    def directed_light_cartesian(self):
        """Get directed light vector from spherical coordinates."""
        theta = self.__directed_light[0]
        phi = self.__directed_light[1]
        r = self.__directed_light[2]
        return array([
            r * sin(theta) * cos(phi),
            r * sin(theta) * sin(phi),
            r * cos(theta)
        ])

    @directed_light.setter
    def directed_light(self, directed_light):
        """Set directed light vector."""
        directed_light = array(directed_light)
        if directed_light.shape != (3,):
            raise ValueError(ERROR_TEXT['LIGHT_DIRECTION']
                             .format(directed_light.shape))
        self.__directed_light = directed_light

    @property
    def ambient_light(self):
        """Get ambient light."""
        return self.__ambient_light

    @ambient_light.setter
    def ambient_light(self, ambient_light):
        """Set ambient light."""
        self.__ambient_light = ambient_light

    @property
    def light(self):
        """Get light vector."""
        return concatenate((self.directed_light, [self.ambient_light]))

    @property
    def light_cartesian(self):
        """Get light from spherical coordinates."""
        return concatenate((self.directed_light_cartesian,
                            [self.ambient_light]))

    @property
    def coefficients(self):
        """Get array of Face coefficients."""
        return self.__coefficients

    @staticmethod
    def from_array(parameters):
        """Create Face from array of parameters."""
        coefficients = parameters[:-4]
        ambient_light = parameters[-4]
        directed_light = parameters[-3:]
        return Face(coefficients=coefficients,
                    directed_light=directed_light,
                    ambient_light=ambient_light)
