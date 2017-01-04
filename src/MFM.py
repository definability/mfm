"""Singleton module for Morphable Face Model manipulations."""
from os.path import isfile

from scipy.io import loadmat
from numpy.random import rand, randn
from numpy.linalg import norm
from numpy import array, fabs, floor, load

from .Face import Face
from .View import View

DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__MODEL = None
__EV_NORMALIZED = None
__DIMENSIONS = None


def init(path=None):
    """Initialize Morphable Face Model singleton.

    Loads information from MatLAB file, chaches triangles, principal components
    and other immutable values used by any Face.
    """
    global __MODEL, __DIMENSIONS, __EV_NORMALIZED

    path = path if path is not None else DEFAULT_MODEL_PATH
    path_npz = '%s.npz' % path
    if isfile(path_npz):
        # savez('mfm.npz', **{x: y for x, y in model.items()
        #                     if x in ['shapeEV', 'shapePC', 'tl', 'shapeMU']})
        __MODEL = load('%s.npz' % path)
    elif isfile(path):
        __MODEL = loadmat(path)
    else:
        raise IOError('Morphable Model Face file `%s` was not found' % path)

    __EV_NORMALIZED = __MODEL['shapeEV'].flatten() / __MODEL['shapeEV'].min()

    principal_components = __MODEL['shapePC'].astype('f')
    triangles = (__MODEL['tl'] - 1).flatten()

    __DIMENSIONS = principal_components.shape[1]

    mean_shape = __MODEL['shapeMU'].astype('f')
    pc_deviations = __MODEL['shapeEV'].astype('f')

    AXES_ORDER = (2, 0, 1)
    mean_shape = __swap_axes(mean_shape, AXES_ORDER)
    principal_components = __swap_axes(principal_components, AXES_ORDER)

    View.set_triangles(triangles)
    View.set_principal_components(principal_components)
    View.set_deviations(pc_deviations)
    View.set_mean_face(mean_shape)
    View.finalize_initialization()


def __swap_axes(points, axes_order):
    """Swap axes of 3D points."""
    vertices = points.shape[0] // 3
    return (points.reshape(vertices, 3, points.shape[1])[:, axes_order, ...]
            .reshape(*points.shape))
    return points


def __random_cos():
    """Generate random real number from [-1; 1]."""
    return 2 * rand() - 1


def get_multipliers(scale=1):
    """Get eigenvalues.

    Values will be normalized to the smallest one
    and multiplied by given number.
    """
    return floor(scale * __EV_NORMALIZED**.5).astype('i')


def get_face(coefficients=None, directed_light=None, ambient_light=None):
    """Produce new face.

    Usage:
    - if coefficients not provided, random Face will be generated.
    - if light parameters not provided, random will be chosen.
    """
    if coefficients is None:
        coefficients = randn(__DIMENSIONS)
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
