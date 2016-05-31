from scipy.io import loadmat
from numpy.random import rand, randn
from numpy import ones, dot

from .Face import Face


DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__model = None
__triangles = None
__triangles_flattened = None

__principal_components = None
__dimensions = None


def init(path=None):
    global __model, __triangles, __triangles_flattened
    global __principal_components, __dimensions

    __model = loadmat(path if path is not None else DEFAULT_MODEL_PATH)
    __triangles = __model['tl'] - 1
    __triangles_flattened = (__model['tl'] - 1).flatten()

    __principal_components = __model['shapePC']
    __dimensions = __principal_components.shape[1]

    Face.set_triangles(__triangles,
                       __triangles_flattened.ctypes.get_as_parameter())


def __random_cos():
    return 2 * rand() - 1


def get_face(coefficients=None, lights=None):
    if coefficients is None:
        coefficients = randn(__dimensions, 1)
    if lights is None:
        lights = (__random_cos(), __random_cos(), __random_cos())

    n_seg = 1 if len(coefficients.shape) == 1 else coefficients.shape[1]

    mean_shape = __model['shapeMU'] * ones([1, n_seg])
    pc_deviations = __model['shapeEV'][0:__dimensions] * ones([1, n_seg])

    features = dot(__principal_components[:, 0:__dimensions],
                   coefficients * pc_deviations)
    vertices = mean_shape + features

    return Face(vertices.astype('f'), lights)
