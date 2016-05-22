from load_model import load_model
from render_triangle import rasterize_triangles

mfm = load_model()

model = {
    'mfm': mfm,
    'triangles': model['tl'] - 1,
    'triangles_flattened': model['tl'].flatten() - 1,
    'light': True,
    'normals': None
}

rasterize_triangles(model)

