from src import Model, Face
from src.fitter import ModelFitter
from tests.dummy import View


def test_constructor():
    assert isinstance(Model(View()), Model)


def test_face_setter():
    view = View()
    model = Model(view)
    face = Face()
    model.face = face
    assert model.face is face
    assert view.face is face


def test_start():
    Model(View()).start(None)
    Model(View()).start(ModelFitter)


def test_close():
    model = Model(View())
    model.start()
    model.close()


def test_redraw():
    model = Model(View())
    model.start(None)
    model.redraw()
    model.redraw(lambda: None)
