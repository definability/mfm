from unittest import TestCase
from numpy import array, allclose

from src import Face

class FaceTest(TestCase):


    def setUp(self):
        vertices = [[1, 0, -1], [0, 0, 0], [-1, 0, 1]]
        normalized_vertices = [[.5, 0, -.5], [0, 0, 0], [-.5, 0, .5]]

        self.original_vertices = array(vertices, dtype='f')
        self.normalized_vertices = array(normalized_vertices, dtype='f')
        self.vertices = self.original_vertices.flatten()


    def tearDown(self):
        pass


    def test_constructor(self):
        self.assertIsInstance(Face(self.vertices), Face)


    def test_get_vertices(self):
        face = Face(self.vertices)
        self.assertTrue(allclose(face.get_vertices(), self.normalized_vertices))

