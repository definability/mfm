from numpy import allclose


from src import Model, Face
from tests.dummy import View


def test_request_image():
    results = []

    face = Face()
    callback = lambda img: results.append(img)
    model = Model(View())

    model.request_image(face, callback)
    assert results == []


def test_receive_image():
    results = []
    face = Face()
    view = View()
    model = Model(view)
    callback = lambda img: results.append(img)
    model.request_image(face, callback)
    view.image = [1, 2, 3, 4]
    view.callback()
    assert allclose(results[0], view.image)


def test_request_images():
    results = []
    images = [[0]*4, [1]*4, [2]*4]

    face = Face()
    view = View()
    model = Model(view)
    callback = lambda img: results.append(img)

    model.request_image(face, callback)
    model.request_image(face, callback)
    assert len(results) == 0


def test_receive_images():
    results = []
    images = [[0]*4, [1]*4, [2]*4]

    face = Face()
    view = View()
    model = Model(view)
    callback = lambda img: results.append(img)

    model.request_image(face, callback)
    model.request_image(face, callback)

    view.image = images[0]
    view.callback()
    assert len(results) == 1
    assert allclose(results[0], images[0])

    view.image = images[1]
    view.callback()
    assert len(results) == 2
    assert allclose(results[1], images[1])

    final_callback = lambda img: results.append([img])
    model.request_image(face, callback)
    view.image = images[2]
    view.callback()
    assert len(results) == 3
    assert allclose(results[2], [images[2]])
