from src.fitter import FittersChain


def test_constructor():
    assert isinstance(FittersChain([], None, None), FittersChain)
