from numpy import allclose

from src import Face


def test_default_coefficients():
    assert Face().coefficients.size == 0


def test_default_scale():
    assert allclose(Face().scale, (1, 1, 1))


def test_default_position():
    assert allclose(Face().position, (0, 0, 1))


def test_default_position_cartesian():
    assert allclose(Face().position_cartesian, (0, 0, 1))


def test_default_directed_light():
    assert allclose(Face().directed_light, (0, 0, 0))


def test_default_directed_light_cartesian():
    assert allclose(Face().directed_light_cartesian, (0, 0, 1))


def test_default_ambient_light():
    assert allclose(Face().ambient_light, 0)


def test_default_light():
    assert allclose(Face().light, (0, 0, 0, 0))


def test_default_light_cartesian():
    assert allclose(Face().light_cartesian, (0, 0, 1, 0))


def test_default_as_array():
    assert Face().as_array.size == Face.NON_PCS_COUNT
