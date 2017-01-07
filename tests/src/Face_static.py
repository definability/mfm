from pytest import fixture
from numpy import allclose, pi, array

from src import Face as __Face


@fixture(scope='module')
def Face():
    __Face.set_initial_rotation(0, 0)
    yield __Face
    __Face.set_initial_rotation(0, 0)


def test_set_initial_rotation(Face):
    Face.set_initial_rotation(pi, pi)
    assert allclose(Face().position_cartesian, (0, 0, -1))
    Face.set_initial_rotation(pi / 2, pi)
    assert allclose(Face().position_cartesian, (0, 0, -1))
    Face.set_initial_rotation(pi, pi / 2)
    assert allclose(Face().position_cartesian, (-1, 0, 0))


def test_from_array(Face):
    direction = (.5, .5, .5)
    scale = (2, 2, 2)
    directed_light = (1, 1, 1)
    coefficients = (0, 1, 2, 3)

    face = Face(position=direction, scale=scale, directed_light=directed_light,
                coefficients=coefficients)
    face_array = face.as_array

    assert allclose(Face.from_array(face_array).position, direction)
    assert allclose(Face.from_array(face_array).scale, scale)
    assert allclose(Face.from_array(face_array).directed_light, directed_light)
    assert allclose(Face.from_array(face_array).coefficients, coefficients)

    assert allclose(Face.from_array(face_array).as_array, face_array)

    assert allclose(face_array[Face.DIRECTION_COMPONENTS_SLICE], direction)
    assert allclose(face_array[Face.LIGHT_COMPONENTS_SLICE], directed_light)
    assert allclose(face_array[Face.SCALE_COMPONENTS_SLICE], scale)
    assert allclose(face_array[:-Face.NON_PCS_COUNT], coefficients)
