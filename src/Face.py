import logging

from numpy import array, zeros, concatenate, sin, cos, arcsin, arccos

ERROR_TEXT = {
    'VERTICES_SIZE': "Size of vertices array should be a multiple of three, "
                     "but {} provided",
    'TRIANGLES_SHAPE': "Need array of triangles (x, 3), "
                       "but array with shape {} provided",
    'TRIANGLES_VERTICES': "Each triangle should contain 3 vertices, "
                          "but {} provided",
    'LIGHT_DIRECTION': "Light should be represented by 3D vector, "
                       "but array of shape {} provided",
    'POSITION': "Position should be represented by 3D vector, "
                "but array of shape {} provided"
}


def spherical_to_cartesian(phi, theta, radius=1.0):
    """Convert spherical coordinates to cartesian.

    Given sinus of polar and azimuthal angle, and radial distance,
    calculate cartesian coordinates of the point.
    """
    sin_phi = sin(phi)
    sin_theta = sin(theta)

    cos_phi = cos(phi)
    cos_theta = cos(theta)

    return array([
        radius * sin_theta * cos_phi,
        radius * sin_theta * sin_phi,
        radius * cos_theta
    ])


class Face:
    """Class to represent Face instances."""

    LIGHT_COMPONENTS_COUNT = 3
    DIRECTION_COMPONENTS_COUNT = 3
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

    __initial_phi = 0.0
    __initial_theta = 0.0

    def __init__(self, ambient_light=0, directed_light=None,
                 position=None, coefficients=None):
        """Create new Face."""
        self.__directed_light = None
        self.__ambient_light = None
        self.__position = None

        self.ambient_light = ambient_light

        if directed_light is None:
            self.directed_light = zeros(3, dtype='f')
        else:
            self.directed_light = directed_light

        if position is None:
            self.position = zeros(3, dtype='f')
        else:
            self.position = position

        if coefficients is None:
            self.__coefficients = array([], dtype='f')
        else:
            self.__coefficients = array(coefficients, dtype='f')

    @property
    def position(self):
        """Get position."""
        return self.__position

    @property
    def position_cartesian(self):
        """Get directed light vector from spherical coordinates."""
        phi = arcsin(self.__position[0]) + Face.__initial_phi
        theta = arcsin(self.__position[1]) + Face.__initial_theta
        return spherical_to_cartesian(phi, theta)

    @position.setter
    def position(self, position):
        """Set position vector."""
        position = array(position)
        if position.shape != (3,):
            raise ValueError(ERROR_TEXT['POSITION']
                             .format(position.shape))
        self.__position = position

    @property
    def directed_light(self):
        """Get directed light vector."""
        return self.__directed_light

    @property
    def directed_light_cartesian(self):
        """Get directed light vector from spherical coordinates."""
        phi = arcsin(self.__directed_light[0]) + Face.__initial_phi
        theta = arcsin(self.__directed_light[1]) + Face.__initial_theta
        return spherical_to_cartesian(phi, theta)

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

    @property
    def as_array(self):
        """Get NumPy array representation of the Face."""
        result = zeros(self.coefficients.size + Face.NON_PCS_COUNT, dtype='f')
        result[Face.NON_PCS_SLICE] = self.coefficients
        result[Face.DIRECTION_COMPONENTS_SLICE] = self.position
        result[Face.LIGHT_COMPONENTS_SLICE] = self.directed_light
        return result

    @staticmethod
    def set_initial_rotation(phi=0.0, theta=0.0):
        """Set initial rotation of Face.

        Given angles will be added to light and rotation vector.
        """
        Face.__initial_phi = phi
        Face.__initial_theta = theta

    @staticmethod
    def from_array(parameters):
        """Create Face from array of parameters."""
        coefficients = parameters[Face.NON_PCS_SLICE]
        position = parameters[Face.DIRECTION_COMPONENTS_SLICE]
        directed_light = parameters[Face.LIGHT_COMPONENTS_SLICE]

        float_format = '{:>6.04}'
        light_format = ', '.join([float_format] * len(directed_light))
        direction_format = ', '.join([float_format] * len(position))
        coefficients_format = ', '.join([float_format] * len(coefficients))

        format_str = ''
        format_str += 'Light: <' + light_format + '>;'
        format_str += ' Direction: <' + direction_format + '>;'
        format_str += ' Coefficients: <' + coefficients_format + '>'
        logging.debug(
            format_str.format(*(directed_light.tolist() + position.tolist()
                              + coefficients.tolist())))

        return Face(coefficients=coefficients,
                    directed_light=directed_light,
                    position=position)
