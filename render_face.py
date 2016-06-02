from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP

from OpenGL.GLUT import glutSpecialUpFunc, glutSpecialFunc, glutKeyboardUpFunc
from OpenGL.GLUT import glutKeyboardFunc, glutPostRedisplay, glutMainLoop

from src import MFM, View


def render_face():
    MFM.init()
    model = {
        'light': True,
        'face': None,
        'view': None
    }
    model['view'] = View((500, 500))
    calculate(model)

    rotations = {
        'x': 0.,
        'y': 0.,
        'z': 0.
    }

    glutKeyboardFunc(lambda key, x, y:
                     keyboard(rotations, key, False, False, model))
    glutKeyboardUpFunc(lambda key, x, y:
                       keyboard(rotations, key, True, False, model))
    glutSpecialFunc(lambda key, x, y:
                    keyboard(rotations, key, False, True, model))
    glutSpecialUpFunc(lambda key, x, y:
                      keyboard(rotations, key, True, True, model))

    glutMainLoop()


def draw(model, rotations):
    vertices = model['face'].get_vertices_c()
    colors = model['face'].get_light_map_c() if model['light'] \
        else model['face'].get_normal_map_c()
    rotation = (rotations['x'], rotations['y'], rotations['z'])

    model['view'].draw(vertices, colors, rotation)


def keyboard(rotations, key, release=False, special=True, model=None):
    directions = {
        True: {
            GLUT_KEY_UP: ('x', -1.),
            GLUT_KEY_DOWN: ('x', 1.),
            GLUT_KEY_RIGHT: ('y', -1.),
            GLUT_KEY_LEFT: ('y', 1.)
        },
        False: {
            b'z': ('z', -1.),
            b'a': ('z', 1.)
        }
    }

    if key in directions[special]:
        axis, value = directions[special][key]
        rotations[axis] = 0. if release else value
        rotation = (rotations['x'], rotations['y'], rotations['z'])
        model['view'].update(rotation=rotation)
    elif not special:
        if key == b'q':
            return model['view'].close()
        if key == b'n' and not release:
            model['light'] = not model['light']
        if key == b'r' and not release:
            return calculate(model)
        calculate(model, False)

    model['view'].redraw()


def calculate(model, new_model=True):
    if new_model:
        model['face'] = MFM.get_face()

    vertices = model['face'].get_vertices_c()
    colors = model['face'].get_light_map_c() if model['light'] \
        else model['face'].get_normal_map_c()

    model['view'].update(vertices, colors)
