from unittest import TestCase
from numpy import array, allclose

from src import ModelFitter


class ModelFitterTest(TestCase):
    def test_constructor(self):
        self.assertIsInstance(ModelFitter(array([])), ModelFitter)

    def test_check(self):
        N = array([[1, 0, 1, 1],
                   [0, 1, 1, 1],
                   [1, 2, 2, 1]])
        light = array([.5, .1, 1., 0.])
        image = N.dot(light)

        fit = ModelFitter(image)
        x = fit.check(N)
        self.assertTrue(allclose(N.dot(x), N.dot(light)))
