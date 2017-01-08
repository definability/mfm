from os import remove

import pytest
from scipy.io import savemat
from numpy import array, zeros, ones

from src import MFM, Face


DATA_FILE = 'data.mat'


@pytest.fixture
def mfm():
    vertices = array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                      [1, 0, 1], [0, 1, 1]], dtype='f')
    triangles = array([[0, 1, 2], [2, 3, 4]], dtype='uint16')

    principal_components = zeros((vertices.size, 199))
    deviations = ones((199, 1))

    savemat(DATA_FILE, {
        'shapeMU': vertices.reshape((vertices.size, 1)),
        'shapePC': principal_components,
        'shapeEV': deviations,
        'tl': triangles + 1
    })
    MFM.init(DATA_FILE)
    yield MFM
    remove(DATA_FILE)


def test_get_face_class(mfm):
    assert isinstance(mfm.get_face(), Face)
