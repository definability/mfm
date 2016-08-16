from unittest import TestCase
from numpy import array

from src.fitter import ModelFitter


class ModelFitterTest(TestCase):

    def test_constructor(self):
        self.assertIsInstance(ModelFitter(array([])), ModelFitter)
