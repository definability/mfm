from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP

from OpenGL.GLUT import glutSpecialUpFunc, glutSpecialFunc, glutKeyboardUpFunc
from OpenGL.GLUT import glutKeyboardFunc

from src import MFM, Model


def render_face():
    MFM.init()

    model = Model()

    rotations = {'x': 0., 'y': 0., 'z': 0.}
    glutKeyboardFunc(lambda key, x, y:
                     keyboard(rotations, key, False, False, model))
    glutKeyboardUpFunc(lambda key, x, y:
                       keyboard(rotations, key, True, False, model))
    glutSpecialFunc(lambda key, x, y:
                    keyboard(rotations, key, False, True, model))
    glutSpecialUpFunc(lambda key, x, y:
                      keyboard(rotations, key, True, True, model))

    model.start()


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
        model.rotate(axis, 0. if release else value)
    elif not special:
        if key == b'q':
            return model.close()
        if key == b'n' and not release:
            model.toggle_texture()
        if key == b'r' and not release:
            return model.calculate()
        model.calculate(False)

    model.redraw()
