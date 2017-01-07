from numpy import allclose

from src import Face

def test_set_position():
    face = Face()
    face.position = (0, 0, 0)
    assert allclose(face.position, (0, 0, 0))
    face.position = (1, 1, 1)
    assert allclose(face.position, (1, 1, 1))


def test_set_directed_light():
    face = Face()
    face.position = (0, 0, 0)
    assert allclose(face.position, (0, 0, 0))
    assert allclose(face.position_cartesian, (0, 0, 1)) 
    face.position = (1, 1, 1)
    assert allclose(face.position, (1, 1, 1))
    assert allclose(face.position_cartesian, (0, 1, 0)) 


def test_set_ambient_light():
    face = Face()
    face.ambient_light = 0
    assert allclose(face.ambient_light, 0)
    face.ambient_light = 1
    assert allclose(face.ambient_light, 1)


def test_set_scale():
    face = Face()
    face.scale = (2, 2, 2)
    assert allclose(face.scale, (2, 2, 2))
    face.scale = (1, 1, 1)
    assert allclose(face.scale, (1, 1, 1))


def test_set_directed_light():
    face = Face()
    face.position = (0, 0, 0)
    assert allclose(face.position, (0, 0, 0))
    face.position = (1, 1, 1)
    assert allclose(face.position, (1, 1, 1))
