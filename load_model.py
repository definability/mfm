import scipy.io as sio
from numpy import ones, dot

DEFAULT_MORPHABLE_MODEL_PATH = '01_MorphableModel.mat'


def load_model(path=DEFAULT_MORPHABLE_MODEL_PATH):
    return sio.loadmat(path)


def get_shape(model, coefficients=None):
    if coefficients is not None:
        shp = morph(model, coefficients)
    else:
        shp = model['shapeMU']
    return shp.reshape((len(shp) / 3, 3)).transpose()


def get_figure(path=DEFAULT_MORPHABLE_MODEL_PATH, coefficients=None):
    model = load_model()
    shape = get_shape(model, coefficients)
    triangles = model['tl'] - 1
    return shape, triangles


def morph(model, coefficients):
    pc = model['shapePC']
    ev = model['shapeEV']
    n_dim = pc.shape[1]
    n_seg = 1 if len(coefficients.shape) == 1 else coefficients.shape[1]
    mu_mat = model['shapeMU'] * ones([1, n_seg])
    pc_mul = dot(pc[:,0:n_dim], (coefficients * (ev[0:n_dim] * ones([1, n_seg]))))
    obj = mu_mat + pc_mul
    return obj

