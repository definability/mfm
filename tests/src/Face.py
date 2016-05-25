from unittest import TestCase
from numpy import array, allclose

from src import Face

class FaceTest(TestCase):


    def setUp(self):
        vertices = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        self.original_vertices = array(vertices, dtype='f')
        self.normalized_vertices = self.original_vertices - 1./3
        self.vertices = self.original_vertices.flatten()
        self.triangles = array([[0, 1, 2]], dtype='uint16')
        self.triangles_c = self.triangles.flatten().ctypes.get_as_parameter()

        Face.set_triangles(self.triangles, self.triangles_c)


    def tearDown(self):
        pass


    def test_constructor(self):
        self.assertIsInstance(Face(self.vertices), Face)


    def test_get_vertices(self):
        face = Face(self.vertices)
        self.assertTrue(allclose(face.get_vertices(), self.normalized_vertices))

