from mayavi import mlab
from load_model import get_figure
from numpy.random import randn

shape, triangles = get_figure(coefficients=randn(199, 1))
mlab.triangular_mesh(shape[0], shape[1], shape[2], triangles, color=(1,1,1))

