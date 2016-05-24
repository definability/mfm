from load_model import load_model
from render_face import render_face
from src import Face

mfm = load_model()

model = {
    'mfm': mfm,
    'light': True,
    'face': None
}
triangles = mfm['tl'] - 1
triangles_flattened = (mfm['tl'] - 1).flatten()
Face.set_triangles(triangles, triangles_flattened.ctypes.get_as_parameter())

render_face(model)

