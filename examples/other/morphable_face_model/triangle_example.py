from load_model import *
from render_triangle import rasterize_triangles

from PIL import Image
from numpy import array, zeros
from numpy.random import randn

from calculations import get_normals, set_light, get_normal_map, centralize

from cProfile import Profile
from pstats import Stats

model = load_model()

redraw = True
light = True
while True:
    profile = Profile()
    profile.enable()

    if redraw:
        lights = None
        normal_map = None

        coordinates = morph(model, randn(199, 1)).astype('f')
        #coordinates = morph(model, zeros(199).reshape(199, 1)).astype('f')
        #coordinates = model['shapeMU']
        points = centralize(coordinates.reshape(coordinates.shape[0]/3, 3))
        triangles = model['tl'] - 1
        normals = get_normals(points, triangles)

    if lights is None and light:
        light_direction = array([-1, 0, -1])/(2**.5)
        lights = set_light(normals, light_direction).astype('f')
    elif normal_map is None and not light:
        normal_map = get_normal_map(normals).astype('f')

    profile.disable()
    Stats(profile).sort_stats('tottime').print_stats()

    colors = lights if light else normal_map
    status = rasterize_triangles(points, triangles.flatten(), colors)
    redraw = True
    if status == 0:
        break
    elif status == 2:
        redraw = False
        light = not light

