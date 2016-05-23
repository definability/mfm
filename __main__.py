from load_model import load_model
from render_face import render_face

mfm = load_model()

model = {
    'mfm': mfm,
    'triangles': mfm['tl'] - 1,
    'triangles_flattened': mfm['tl'].flatten() - 1,
    'light': True,
    'normals': None
}

render_face(model)

