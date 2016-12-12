
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

    LIGHT_COMPONENTS_COUNT = 3
    DIRECTION_COMPONENTS_COUNT = 0 # 3
    NON_PCS_COUNT = LIGHT_COMPONENTS_COUNT + DIRECTION_COMPONENTS_COUNT

    DIRECTION_COMPONENTS_START = - (LIGHT_COMPONENTS_COUNT
        + DIRECTION_COMPONENTS_COUNT)
    DIRECTION_COMPONENTS_END = (DIRECTION_COMPONENTS_START
        + DIRECTION_COMPONENTS_COUNT)
    LIGHT_COMPONENTS_START = DIRECTION_COMPONENTS_END
    LIGHT_COMPONENTS_END = LIGHT_COMPONENTS_START + LIGHT_COMPONENTS_COUNT

    NON_PCS_SLICE = slice(0, - NON_PCS_COUNT)
    LIGHT_COMPONENTS_SLICE = slice(LIGHT_COMPONENTS_START,
                                   LIGHT_COMPONENTS_END or None)
    DIRECTION_COMPONENTS_SLICE = slice(DIRECTION_COMPONENTS_START,
                                       DIRECTION_COMPONENTS_END or None)

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
            self.__coefficients = array(coefficients, dtype='f')

    @property
    def directed_light(self):
        """Get directed light vector."""
        return self.__directed_light

    @property
    def directed_light_cartesian(self):
        """Get directed light vector from spherical coordinates."""
        phi = self.__directed_light[0]
        theta = self.__directed_light[1]
        if False:
            sin_theta = sin(theta)
            cos_theta = cos(theta)
            sin_phi = sin(phi)
            cos_phi = cos(phi)
        else:
            sin_theta = theta
            cos_theta = (1 - theta**2)**.5
            sin_phi = phi
            cos_phi = (1 - phi**2)**.5
        r = 1. #self.__directed_light[2]
        return array([
            r * sin_theta * cos_phi,
            r * sin_theta * sin_phi,
            r * cos_theta
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
                            [self.directed_light[2]]))

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
