from warnings import warn

from numpy import array, dot, zeros_like, mean, apply_along_axis, column_stack
from numpy import concatenate
import numpy

from .normals import get_normals

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


def normalize(vertices):
    warn('Shaders will zoom it', DeprecationWarning)
    vertices = vertices.reshape(vertices.size // 3, 3)
    vertices = vertices - vertices.min()
    vertices /= vertices.max()
    vertices -= apply_along_axis(mean, 0, vertices)
    return vertices


class Face:

    __triangles = None
    __triangles_flattened = None
    __triangles_c = None

    def __init__(self, vertices, directed_light=None, constant_light=0,
                 coefficients=None, need_normalize=True):
        """Create new Face.

        Vertices are connected by triangles.
        Coefficients needed to generate new Face based on existent one,
        if we need to change few parameters and it will be more efficient
        than recalculate new Face.
        """
        if vertices.size % 3 != 0:
            raise ValueError(ERROR_TEXT['VERTICES_SIZE'].format(vertices.size))
        vertices = vertices.astype('f')
        self.__original_vertices = vertices.copy()
        if need_normalize:
            self.__vertices = normalize(vertices)
        else:
            self.__vertices = vertices.reshape(vertices.size // 3, 3)
        self.__vertices_c = self.__vertices.ctypes.get_as_parameter()
        self.__light_map = None
        self.__directed_light = None
        self.__constant_light = constant_light
        if directed_light is not None:
            self.set_light(directed_light, constant_light)
        self.__coefficients = coefficients

        self.__normals = None
        self.__normal_map = None

        self.__normal_max = None
        self.__normal_min = None

    def get_coefficients(self):
        """Get coefficients for eigenvectors of current Face."""
        return self.__coefficients

    def get_original_vertices(self):
        """Get not normalized vertices.

        Handy for creation of new Face based on this one.
        """
        warn('Will be calculated by shaders', DeprecationWarning)
        return self.__original_vertices

    def get_vertices(self):
        """Get normalized vertices."""
        warn('Will be calculated by shaders', DeprecationWarning)
        return self.__vertices

    def get_vertices_c(self):
        """Get C array of normalized vertices."""
        warn('Shaders don\'t need C array', DeprecationWarning)
        return self.__vertices_c

    @staticmethod
    def get_triangles_c():
        """Get C array of indices of vertices connected in triangles."""
        warn('Shaders don\'t need C array', DeprecationWarning)
        return Face.__triangles_c

    @staticmethod
    def get_triangles():
        """Get NumPy matrix indices of vertices connected in triangles."""
        return Face.__triangles

    def get_directed_light(self):
        """Get directed light vector."""
        warn('Use property instead', DeprecationWarning)
        return self.__directed_light

    def get_constant_light(self):
        """Get ambient light intencity."""
        warn('Use property ambient_light instead', DeprecationWarning)
        return self.__constant_light

    def get_light_map(self):
        """Get array with intensities of vertices.

        Dot product of normal vectors and directed light calculated
        and cropped to [0; 1] bounds.
        Then ambient light is added and cropped again.

        Result contains array of 3-arrays for each of RGB channel.
        """
        warn('Shadows are calculated by shaders', DeprecationWarning)
        if self.__light_map is not None:
            return self.__light_map

        self.__light_map = dot(self.get_normals(), self.__directed_light)
        self.__light_map[self.__light_map < 0.] = 0.
        self.__light_map += self.__constant_light
        self.__light_map[self.__light_map > 1.] = 1.
        self.__light_map = column_stack([self.__light_map.astype('f')]*3)

        return self.__light_map

    def get_light_map_c(self):
        """Get C array with light map."""
        warn('Shadows are calculated by shaders', DeprecationWarning)
        return self.get_light_map().ctypes.get_as_parameter()

    def get_normal_map_c(self):
        """Get C array with normal vectors map."""
        warn('Normal maps are drawn by shaders', DeprecationWarning)
        return self.get_normal_map().ctypes.get_as_parameter()

    def get_normals(self):
        """Get normal vectors for each vertex.

        Normal vector calculated for each triangle.
        Normal vector of each vertex is normalized to |n| = 1.0
        sum of normal vectors of triangles, which contain this point.
        """
        warn('Normal maps are calculated by shaders', DeprecationWarning)
        if self.__normals is not None:
            return self.__normals

        self.__normals = get_normals(self.__vertices,
                                     self.__triangles_flattened)
        return self.__normals

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
        return self.__constant_light

    @ambient_light.setter
    def ambient_light(self, ambient_light):
        self.__constant_light = ambient_light

    @property
    def light(self):
        return concatenate((self.directed_light, [self.ambient_light]))

    @property
    def normal_min(self):
        return self.__normal_min

    @normal_min.setter
    def normal_min(self, normal_min):
        self.__normal_min = normal_min

    @property
    def normal_max(self):
        return self.__normal_max

    @normal_max.setter
    def normal_max(self, normal_max):
        self.__normal_max = normal_max

    def get_normal_map(self):
        """Get normal map for each vertex.

        Normal map contains componentwise normalized to [0; 1]
        normal vectors of each vertex to be represented as colors.
        """
        warn('Normal maps are drawn by shaders', DeprecationWarning)
        if self.__normal_map is not None:
            return self.__normal_map

        self.__normal_map = self.get_normals().copy()

        self.__normal_min = apply_along_axis(numpy.min, 0, self.__normal_map)
        self.__normal_map -= self.__normal_min

        self.__normal_max = apply_along_axis(numpy.max, 0, self.__normal_map)
        self.__normal_map /= self.__normal_max

        self.__normal_map = self.__normal_map.astype('f')

        return self.__normal_map

    def normal_map_to_normal_vectors(self, normal_map):
        """Convert normal map to normal vectors.

        Image RGB channels cannot contain negative values,
        but it's necessary to have normal vectors of each point
        for fitting procedure.
        This method accepts normal map of the Face
        and performs denormalization.
        """
        warn('Normal maps will not be used', DeprecationWarning)
        return (normal_map * self.__normal_max) + self.__normal_min

    def set_light(self, directed_light=None, constant_light=None):
        """Change light conditions of the Face."""
        warn('Use properties instead', DeprecationWarning)
        if directed_light is not None:
            directed_light = array(directed_light)
            if directed_light.shape != (3,):
                raise ValueError(ERROR_TEXT['LIGHT_DIRECTION']
                                 .format(directed_light.shape))
            self.__directed_light = directed_light
        if constant_light is not None \
                and constant_light > -2 and constant_light < 2:
            self.__constant_light = constant_light
        self.__light_map = None

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
