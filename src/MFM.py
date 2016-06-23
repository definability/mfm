from scipy.io import loadmat
from numpy.random import rand, randn
from numpy.linalg import norm
from numpy import array, ones, dot, fabs

from .Face import Face
from .View import View


DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__model = None
__triangles = None
__triangles_flattened = None
__triangles_c = None

__principal_components = None
__principal_components_flattened = None
__dimensions = None


def init(path=None):
    global __model, __triangles, __triangles_flattened, __dimensions
    global __principal_components, __principal_components_flattened

    __model = loadmat(path if path is not None else DEFAULT_MODEL_PATH)
    __triangles = __model['tl'] - 1
    __triangles_flattened = (__model['tl'] - 1).flatten()
    __triangles_c = __triangles_flattened.ctypes.get_as_parameter()

    __principal_components = __model['shapePC']
    __principal_components_flattened = __principal_components.flatten()
    __dimensions = __principal_components.shape[1]

    Face.set_triangles(__triangles, __triangles_c)
    View.set_triangles(__triangles_c, __triangles.size)


def __random_cos():
    return 2 * rand() - 1


def get_face(coefficients=None, directed_light=None, constant_light=None):
    if coefficients is None:
        coefficients = randn(__dimensions, 1)
    coefficients = coefficients.reshape((coefficients.size, 1))
    if directed_light is None:
        directed_light = -fabs(array([__random_cos(), __random_cos(),
                                      __random_cos()]))
        if norm(directed_light) > 0:
            directed_light /= norm(directed_light)
    if constant_light is None:
        constant_light = __random_cos()

    n_seg = 1 if len(coefficients.shape) == 1 else coefficients.shape[1]

    mean_shape = __model['shapeMU'] * ones([1, n_seg])
    pc_deviations = __model['shapeEV'][0:__dimensions] * ones([1, n_seg])

    features = dot(__principal_components[:, 0:__dimensions],
                   coefficients * pc_deviations)
    vertices = mean_shape + features

    return Face(vertices.astype('f'), directed_light, constant_light)
