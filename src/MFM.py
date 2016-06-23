import ctypes
from scipy.io import loadmat
from numpy.random import rand, randn
from numpy.linalg import norm
from numpy import array, ones, dot, fabs, zeros, floor

from .Face import Face
from .View import View

c_face = ctypes.cdll.LoadLibrary('./lib_face.so')

DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__model = None
__triangles = None
__triangles_flattened = None
__triangles_c = None

__principal_components = None
__principal_components_flattened = None
__ev_normalized = None
__dimensions = None


def init(path=None):
    global __model, __triangles, __triangles_flattened, __dimensions
    global __principal_components, __principal_components_flattened
    global __ev_normalized

    __model = loadmat(path if path is not None else DEFAULT_MODEL_PATH)
    __triangles = __model['tl'] - 1
    __triangles_flattened = (__model['tl'] - 1).flatten()
    __triangles_c = __triangles_flattened.ctypes.get_as_parameter()

    __principal_components = __model['shapePC']
    __principal_components_flattened = __principal_components.flatten()
    __dimensions = __principal_components.shape[1]

    __ev_normalized = __model['shapeEV'].flatten() / __model['shapeEV'].min()

    Face.set_triangles(__triangles, __triangles_c)
    View.set_triangles(__triangles_c, __triangles.size)


def __random_cos():
    return 2 * rand() - 1

def get_multipliers(scale=1):
    for m in floor(scale * __ev_normalized).astype('i'):
        yield m

def get_face(coefficients=None, directed_light=None, constant_light=None):
    if coefficients is None:
        coefficients = randn(__dimensions)
    if directed_light is None:
        directed_light = -fabs(array([__random_cos(), __random_cos(),
                                      __random_cos()]))
        if norm(directed_light) > 0:
            directed_light /= norm(directed_light)
    if constant_light is None:
        constant_light = __random_cos()

    if len(coefficients.shape) == 1:
        mean_shape = __model['shapeMU']
        pc_deviations = __model['shapeEV']
        points = __principal_components.shape[0]
        vertices = zeros((points, 1), dtype='f')

        coefficients_f = coefficients.astype('f')

        c_face.get_face(
               mean_shape.ctypes.get_as_parameter(),
               __principal_components_flattened.ctypes.get_as_parameter(),
               pc_deviations.ctypes.get_as_parameter(),
               coefficients_f.ctypes.get_as_parameter(),
               vertices.ctypes.get_as_parameter(),
               __dimensions,
               points)

        return Face(vertices, directed_light, constant_light)
    else:
        coefficients = coefficients.reshape((coefficients.size, 1))
        n_seg = coefficients.shape[1]

        mean_shape = __model['shapeMU'] * ones([1, n_seg])
        pc_deviations = __model['shapeEV'][0:__dimensions] * ones([1, n_seg])

        features = dot(__principal_components[:, 0:__dimensions],
                       coefficients * pc_deviations)

        features = __principal_components.dot(coefficients * pc_deviations)
        vertices = mean_shape + features

        return Face(vertices.astype('f'), directed_light, constant_light)
