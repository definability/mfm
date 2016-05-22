from load_model import load_model
from render_face import render_face

mfm = load_model()

model = {
    'mfm': mfm,
    'triangles': model['tl'] - 1,
    'triangles_flattened': model['tl'].flatten() - 1,
    'light': True,
    'normals': None
}

render_face(model)

