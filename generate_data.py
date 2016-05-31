from scipy.io import savemat
from numpy import array, zeros

vertices = array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                  [1, 0, 1], [0, 1, 1]], dtype='f')
triangles = array([[0, 1, 2], [2, 3, 4]], dtype='uint16')

principal_components = zeros((vertices.size, 199))
deviations = zeros((199, 1))

savemat('data', {
    'shapeMU': vertices.reshape((vertices.size, 1)),
    'shapePC': principal_components,
    'shapeEV': deviations,
    'tl': triangles + 1
})
