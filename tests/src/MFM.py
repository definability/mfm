from os import remove

from unittest import TestCase
from scipy.io import savemat
from numpy import array, allclose, column_stack, zeros

from src import MFM, Face


DATA_FILE = 'data.mat'


class MFMTest(TestCase):

    @classmethod
    def setUpClass(cls):
        vertices = array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                          [1, 0, 1], [0, 1, 1]], dtype='f')
        triangles = array([[0, 1, 2], [2, 3, 4]], dtype='uint16')

        principal_components = zeros((vertices.size, 199))
        deviations = zeros((199, 1))

        savemat(DATA_FILE, {
            'shapeMU': vertices.reshape((vertices.size, 1)),
            'shapePC': principal_components,
            'shapeEV': deviations,
            'tl': triangles + 1
        })
        MFM.init(DATA_FILE)

    def tearDownClass():
        remove(DATA_FILE)

    def test_get_face_class(self):
        self.assertIsInstance(MFM.get_face(), Face)

    def test_get_face_light(self):
        face = MFM.get_face()
        face.set_light([1, 0, 0])
        light_vec = [1., 1., 2**(-.5), 0., 0.]
        light_map = column_stack([light_vec]*3)
        self.assertTrue(allclose(face.get_light_map(), light_map))
