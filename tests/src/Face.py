from unittest import TestCase
from numpy import array, allclose, array_equal, column_stack

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


    def test_set_triangles(self):
        Face.set_triangles(self.triangles, self.triangles_c)
        self.assertTrue(array_equal(Face.get_triangles(), self.triangles))
        self.assertEqual(Face.get_triangles_c(), self.triangles_c)


    def test_get_normals(self):
        face = Face(self.vertices)
        self.assertTrue(allclose(face.get_normals(), 3.**(-.5)))


    def test_get_normal_map(self):
        vertices = array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                          [1, 0, 1], [0, 1, 1]], dtype='f')
        face = Face(vertices)

        triangles = array([[0, 1, 2], [2, 3, 4]], dtype='uint16')
        triangles_c = triangles.flatten().ctypes.get_as_parameter()
        Face.set_triangles(triangles, triangles_c)

        hard_element = (2 / ((1+1+2**2)**.5) - 3**(-.5)) / (1 - 3**(-.5))
        ooz = [1., 1., 0.]
        zzo = [0., 0., 1.]
        normal_map = [ooz, ooz,
                      [2**(-.5), 2**(-.5), hard_element],
                      zzo, zzo]

        self.assertTrue(allclose(face.get_normal_map(), normal_map))


    def test_get_light_map(self):
        vertices = array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                          [1, 0, 1], [0, 1, 1]], dtype='f')
        face = Face(vertices)

        triangles = array([[0, 1, 2], [2, 3, 4]], dtype='uint16')
        triangles_c = triangles.flatten().ctypes.get_as_parameter()
        Face.set_triangles(triangles, triangles_c)

        face.set_light([1, 0, 0])
        light_vec = [1., 1., 2**(-.5), 0., 0.]
        light_map = column_stack([light_vec]*3)
        self.assertTrue(allclose(face.get_light_map(), light_map))
