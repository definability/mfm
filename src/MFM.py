from warnings import warn
import ctypes
from scipy.io import loadmat
from numpy.random import rand, randn
from numpy.linalg import norm
from numpy import array, ones, dot, fabs, zeros, floor

from .Face import Face
from .View import View
from .face import init_face_calculator, calculate_face, calculate_row

DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__model = None
__triangles = None
__triangles_flattened = None
__triangles_c = None

__principal_components = None
__principal_components_flattened = None
__ev_normalized = None
__dimensions = None
__mean_shape = None
__pc_deviations = None


def init(path=None):
    """Initialize Morphable Face Model singleton.

    Loads information from MatLAB file, chaches triangles, principal components
    and other immutable values used by any Face.
    """
    global __model, __triangles, __triangles_flattened, __dimensions
    global __principal_components, __principal_components_flattened
    global __ev_normalized, __mean_shape, __pc_deviations

    __model = loadmat(path if path is not None else DEFAULT_MODEL_PATH)
    __triangles = __model['tl'] - 1
    __triangles_flattened = (__model['tl'] - 1).flatten()
    __triangles_c = __triangles_flattened.ctypes.get_as_parameter()

    __principal_components = __model['shapePC'].astype('f')
    __principal_components_flattened = __principal_components.flatten()
    __dimensions = __principal_components.shape[1]

    __ev_normalized = __model['shapeEV'].flatten() / __model['shapeEV'].min()
    __mean_shape = __model['shapeMU'].astype('f')
    __pc_deviations = __model['shapeEV'].astype('f')

    init_face_calculator(__mean_shape, __principal_components_flattened,
                         __pc_deviations)
    Face.set_triangles(__triangles, __triangles_c)
    View.set_triangles(__triangles_c, __triangles.size)
    View.set_principal_components(__principal_components)
    View.set_deviations(__pc_deviations)
    View.set_mean_face(__mean_shape)


def __random_cos():
    """Generate random real number from [-1; 1]."""
    return 2 * rand() - 1


def get_multipliers(scale=1):
    """Get eigenvalues.

    Values will be normalized to the smallest one
    and multiplied by given number.
    """
    return floor(scale * __ev_normalized**.5).astype('i')


def get_face(coefficients=None, directed_light=None, ambient_light=None):
    """Produce new face.

    Usage:
    - if coefficients not provided, random Face will be generated.
    - if light parameters not provided, random will be chosen.
    """
    if coefficients is None:
        coefficients = randn(__dimensions)
    if directed_light is None:
        directed_light = array([__random_cos(), __random_cos(),
                                fabs(__random_cos())])
        if norm(directed_light) > 0:
            directed_light /= norm(directed_light)
    if ambient_light is None:
        ambient_light = fabs(__random_cos())

    return Face(directed_light=directed_light,
                ambient_light=ambient_light,
                coefficients=coefficients)
