import ctypes

from numpy import array, cross, dot, zeros_like, mean, zeros
from numpy import apply_along_axis, column_stack
import numpy

c_cross = ctypes.cdll.LoadLibrary('./lib_cross.so')

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
    vertices = vertices.reshape(vertices.size // 3, 3)
    vertices = vertices - vertices.min()
    vertices /= vertices.max()
    vertices -= apply_along_axis(mean, 0, vertices)
    return vertices


class Face:

    __triangles = None
    __triangles_c = None

    def __init__(self, vertices, directed_light=None, constant_light=0):
        if vertices.size % 3 != 0:
            raise ValueError(ERROR_TEXT['VERTICES_SIZE'].format(vertices.size))
        self.__vertices = normalize(vertices)
        self.__vertices_c = self.__vertices.ctypes.get_as_parameter()
        self.__light_map = None
        self.__directed_light = None
        self.__constant_light = constant_light
        if directed_light is not None:
            self.set_light(directed_light, constant_light)

        self.__normals = None
        self.__normal_map = None

        self.__normal_max = None
        self.__normal_min = None

    def get_vertices(self):
        return self.__vertices

    def get_vertices_c(self):
        return self.__vertices_c

    @staticmethod
    def get_triangles_c():
        return Face.__triangles_c

    @staticmethod
    def get_triangles():
        return Face.__triangles

    def get_directed_light(self):
        return self.__directed_light

    def get_constant_light(self):
        return self.__constant_light

    def get_light_map(self):
        if self.__light_map is not None:
            return self.__light_map

        self.__light_map = dot(self.get_normals(), self.__directed_light)
        self.__light_map[self.__light_map < 0.] = 0.
        self.__light_map += self.__constant_light
        self.__light_map[self.__light_map > 1.] = 1.
        self.__light_map = column_stack([self.__light_map.astype('f')]*3)

        return self.__light_map

    def get_light_map_c(self):
        return self.get_light_map().ctypes.get_as_parameter()

    def get_normal_map_c(self):
        return self.get_normal_map().ctypes.get_as_parameter()

    def get_normals(self):
        if self.__normals is not None:
            return self.__normals

        self.__normals = zeros_like(self.__vertices)
        c_cross.get_normals(self.__vertices_c, self.__triangles_c,
                            self.__normals.ctypes.get_as_parameter(),
                            len(self.__vertices), len(self.__triangles))
        return self.__normals

    def get_normal_map(self):
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
        print(normal_map.shape, (normal_map * self.__normal_max).shape)
        return (normal_map * self.__normal_max) + self.__normal_min

    def set_light(self, directed_light=None, constant_light=None):
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
        if triangles is not None:
            if len(triangles.shape) != 2:
                raise ValueError(ERROR_TEXT['TRIANGLES_SHAPE']
                                 .format(triangles.shape))
            elif triangles.shape[1] != 3:
                raise ValueError(ERROR_TEXT['TRIANGLES_VERTICES']
                                 .format(triangles.shape[1]))
            Face.__triangles = triangles
        if triangles_c is not None:
            Face.__triangles_c = triangles_c
