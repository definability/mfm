from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP

from OpenGL.GLUT import glutSpecialUpFunc, glutSpecialFunc, glutKeyboardUpFunc
from OpenGL.GLUT import glutKeyboardFunc


class ModelInput:
    __special_keys = {
        GLUT_KEY_UP: ('x', -1.),
        GLUT_KEY_DOWN: ('x', 1.),
        GLUT_KEY_RIGHT: ('y', -1.),
        GLUT_KEY_LEFT: ('y', 1.)
    }
    __keys = {
        b'z': ('z', -1.),
        b'a': ('z', 1.)
    }
    __light_keys = {
        b'h': ('x', .1),
        b'l': ('x', -.1),
        b'j': ('y', .1),
        b'k': ('y', -.1),
    }

    def __init__(self, model):
        self.__model = model

        glutKeyboardFunc(lambda key, x, y: self.__handle_special(key, False))
        glutKeyboardUpFunc(lambda key, x, y: self.__handle_special(key, True))
        glutSpecialFunc(lambda key, x, y: self.__handle_key(key, False))
        glutSpecialUpFunc(lambda key, x, y: self.__handle_key(key, True))

    def __handle_key(self, key, release=False):
        if key in ModelInput.__special_keys:
            self.__rotate(ModelInput.__special_keys, key, release)
        else:
            return
        self.__model.redraw()

    def __handle_special(self, key, release=False):
        if key in ModelInput.__keys:
            self.__rotate(ModelInput.__keys, key, release)
        elif key in ModelInput.__light_keys and not release:
            directed_light = {
                'x': 0.,
                'y': 0.,
                'z': 0.
            }
            axis, value = ModelInput.__light_keys[key]
            directed_light[axis] = value
            self.__model.change_light(direction=directed_light)
        elif key == b'n' and not release:
            self.__model.toggle_texture()
            self.__model.calculate(False)
        elif key == b'r' and not release:
            self.__model.calculate()
            self.__model.redraw()
            return
        elif key == b'q' and not release:
            self.__model.close()
            return
        else:
            return
        self.__model.redraw()

    def __rotate(self, commands, key, release):
        assert key in commands
        axis, value = commands[key]
        self.__model.rotate(axis, 0. if release else value)
        self.__model.calculate(False)
