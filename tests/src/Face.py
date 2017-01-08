from itertools import product

from pytest import raises
from pytest import mark

from src import Face


def test_constructor():
    assert isinstance(Face(), Face)


@mark.parametrize(('name', 'value'),
    product(('scale', 'directed_light', 'position'),
            [0, 'a', ('a', 'b', 'c'), (1, 2, 3, 4), [0.0, 0.0]]))
def test_constructor_wrong_vector3d(name, value):
    with raises(ValueError):
        Face(**{name: value})


@mark.parametrize('value', [0, ['a'], ['a', 'b', 'c']])
def test_constructor_wrong_coefficients(value):
    with raises(ValueError):
        Face(coefficients=value)
