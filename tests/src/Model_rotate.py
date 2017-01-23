from itertools import product

from pytest import fixture
from pytest import mark
from numpy import allclose

from src import Model, Face
from src.fitter import ModelFitter
from tests.dummy import View


@fixture(scope='function')
def model():
    view = View()
    face = Face()
    model = Model(view)
    model.face = face
    yield model


@mark.parametrize(('constrained', 'rotation', 'valid'), [
    (False, (0, 0, 0), True),
    (True, (0, 0, 0), True),
    (False, (1, 0, -1), True),
    (True, (1, 0, -1), True),
    (False, (1, 0, 2), True),
    (True, (1, 0, 2), True),
    (False, (1, 2, 3), True),
    (True, (1, 2, 3), False),
])
def test_rotate(model, constrained, rotation, valid):
    result_light = rotation if valid else (0, 0, 0)
    result = result_light[0], result_light[1], result_light[2] + 1
    rotation = {
        'x': rotation[0],
        'y': rotation[1],
        'z': rotation[2]
    }

    assert allclose(model.face.position, (0, 0, 1))
    model.rotate(rotation, constrained)
    assert allclose(model.face.position, result)

    assert allclose(model.face.directed_light, (0, 0, 0))
    model.change_light(direction=rotation, check_constraints=constrained)
    assert allclose(model.face.directed_light, result_light)


def test_change_light_intensity(model):
    assert allclose(model.face.ambient_light, 0)
    model.change_light(intensity=1)
    assert allclose(model.face.ambient_light, 1)
