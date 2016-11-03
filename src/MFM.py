from os.path import isfile

from scipy.io import loadmat
from numpy.random import rand, randn
from numpy.linalg import norm
from numpy import array, fabs, floor, load

from .Face import Face
from .View import View

DEFAULT_MODEL_PATH = '01_MorphableModel.mat'

__model = None
__ev_normalized = None
__dimensions = None


def init(path=None):
    """Initialize Morphable Face Model singleton.

    Loads information from MatLAB file, chaches triangles, principal components
    and other immutable values used by any Face.
    """
    global __model, __dimensions, __ev_normalized

    path = path if path is not None else DEFAULT_MODEL_PATH
    path_npz = '%s.npz'%path
    if isfile(path):
        # savez('mfm.npz', **{x: y for x, y in model.items()
        #                     if x in ['shapeEV', 'shapePC', 'tl', 'shapeMU']})
        __model = load('%s.npz'%path)
    elif isfile(path_npz):
        __model = loadmat(path)
    else:
        raise IOError('Morphable Model Face file `%s` was not found'%path)

    __ev_normalized = __model['shapeEV'].flatten() / __model['shapeEV'].min()

    principal_components = __model['shapePC'].astype('f')
    triangles = (__model['tl'] - 1).flatten()

    __dimensions = principal_components.shape[1]

    mean_shape = __model['shapeMU'].astype('f')
    pc_deviations = __model['shapeEV'].astype('f')

    View.set_triangles(triangles)
    View.set_principal_components(principal_components)
    View.set_deviations(pc_deviations)
    View.set_mean_face(mean_shape)


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
