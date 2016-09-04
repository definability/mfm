from unittest import TestCase

from src.fitter import FittersChain


class ModelFitterTest(TestCase):

    def test_constructor(self):
        self.assertIsInstance(FittersChain([], None, None), FittersChain)
