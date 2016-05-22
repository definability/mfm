from numpy import array, cross, dot, apply_along_axis, zeros_like, mean, column_stack
from numpy.linalg import norm
from numpy import min as np_min, max as np_max

import ctypes

c_cross = ctypes.cdll.LoadLibrary('./lib_cross.so')

def get_normals(points, triangles):
    vertices = points[triangles]

    first_edges = vertices[:,1] - vertices[:,0]
    second_edges = vertices[:,2] - vertices[:,0]

    normal_vectors = cross(first_edges, second_edges).astype('f')

    result = zeros_like(points)

    nv = normal_vectors.flatten()
    tr = triangles.flatten()

    c_cross.normals(nv.ctypes.get_as_parameter(),
                    tr.ctypes.get_as_parameter(),
                    result.ctypes.get_as_parameter(),
                    len(triangles))
    c_cross.normalize(result.ctypes.get_as_parameter(), len(result))

    return result

def set_light(normals, n):
    result = dot(normals, n)
    result -= result.min()
    result /= result.max()
    return column_stack((result, result, result))

def get_normal_map(normals):
    result = normals - apply_along_axis(np_min, 0, normals)
    return result / apply_along_axis(np_max, 0, result)

def get_center(points):
    return apply_along_axis(mean, 0, points)

def centralize(points):
    return points - get_center(points)

