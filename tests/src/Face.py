from unittest import TestCase
from numpy import array, allclose, array_equal, column_stack, zeros, ones

from src import Face


class FaceTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        self.assertIsInstance(Face(), Face)
