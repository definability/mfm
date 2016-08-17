from unittest import TestCase

from src import Face


class FaceTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        self.assertIsInstance(Face(), Face)
