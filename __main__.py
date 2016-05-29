from load_model import load_model
from render_face import render_face
from src import Face

MFM = load_model()

MODEL = {
    'mfm': MFM,
    'light': True,
    'face': None
}
TRIANGLES = MFM['tl'] - 1
TRIANGLES_FLATTENED = (MFM['tl'] - 1).flatten()
Face.set_triangles(TRIANGLES, TRIANGLES_FLATTENED.ctypes.get_as_parameter())

render_face(MODEL)

