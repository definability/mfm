from numpy import array

from src.fitter import ModelFitter


def test_constructor():
    assert isinstance(ModelFitter(array([])), ModelFitter)
