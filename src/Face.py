from numpy import array, cross, dot, zeros_like, mean
from numpy import apply_along_axis, column_stack
from numpy.linalg import norm
import numpy as np
import ctypes

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


def __normalize(vertices):
    vertices = vertices.reshape(vertices.size // 3, 3)
    vertices = vertices - vertices.min()
    vertices /= vertices.max()
    vertices -= apply_along_axis(mean, 0, vertices)
    return vertices


class Face:

    __triangles = None
    __triangles_c = None


    def __init__(self, vertices, lights=None):
        if vertices.size % 3 != 0:
            raise ValueError(ERROR_TEXT['VERTICES_SIZE'].format(vertices.size))
        self.__vertices = __normalize(vertices)
        self.__vertices_c = self.__vertices.ctypes.get_as_parameter()
        self.__points = None
        self.__light_map = None
        if lights is not None:
            self.set_light(lights)
        else:
            self.__lights = None
        self.__normals = None
        self.__normal_map = None


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


    def get_light_map(self):
        if self.__light_map is not None:
            return self.__light_map

        self.__light_map = dot(self.get_normals(), self.__light)
        self.__light_map -= self.__light_map.min()
        self.__light_map /= self.__light_map.max()
        self.__light_map /= self.__light_map.max()
        self.__light_map = column_stack([self.__light_map.astype('f')]*3)

        return self.__light_map


    def get_light_map_c(self):
        return self.get_light_map().ctypes.get_as_parameter()


    def get_normal_map_c(self):
        return self.get_normal_map().ctypes.get_as_parameter()


    def get_normals(self):
        if self.__normals is not None:
            return self.__normals

        if self.__points is None:
            assert(self.__triangles is not None)
            self.__points = self.__vertices[self.__triangles]

        first_edges = self.__points[:,1] - self.__points[:,0]
        second_edges = self.__points[:,2] - self.__points[:,0]

        normal_vectors = cross(first_edges, second_edges).astype('f')
        normal_vectors_c = normal_vectors.ctypes.get_as_parameter()

        self.__normals = zeros_like(self.__vertices)
        normals_c = self.__normals.ctypes.get_as_parameter()

        c_cross.normals(normal_vectors_c, self.__triangles_c, normals_c,
                        len(self.__triangles))
        c_cross.normalize(normals_c, len(self.__normals))
        return self.__normals


    def get_normal_map(self):
        if self.__normal_map is not None:
            return self.__normal_map

        self.__normal_map = self.get_normals().copy()
        self.__normal_map -= apply_along_axis(np.min, 0, self.__normal_map)
        self.__normal_map /= apply_along_axis(np.max, 0, self.__normal_map)
        self.__normal_map = self.__normal_map.astype('f')

        return self.__normal_map


    def set_light(self, light):
        light = array(light)
        if light.shape != (3,):
            raise ValueError(ERROR_TEXT['LIGHT_DIRECTION'].format(light.shape))
        self.__light = light / norm(light)
        self.__light_map = None
        assert(self.__light.size == 3)


    @staticmethod
    def set_triangles(triangles=None, triangles_c=None):
        if triangles is not None:
            if len(triangles.shape) != 2:
                raise ValueError(ERROR_TEXT['TRIANGLES_SHAPE'] \
                                 .format(triangles.shape))
            elif triangles.shape[1] != 3:
                raise ValueError(ERROR_TEXT['TRIANGLES_VERTICES'] \
                                 .format(triangles.shape[1]))
            Face.__triangles = triangles
        if triangles_c is not None:
            Face.__triangles_c = triangles_c

