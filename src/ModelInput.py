from time import mktime
from datetime import datetime
from os.path import join

from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP

from OpenGL.GLUT import glutSpecialUpFunc, glutSpecialFunc, glutKeyboardUpFunc
from OpenGL.GLUT import glutKeyboardFunc


class ModelInput:
    """Process input and trigger needed methods of Model."""
    __rotation_keys = {
        GLUT_KEY_UP: ('x', -1.),
        GLUT_KEY_DOWN: ('x', 1.),
        GLUT_KEY_RIGHT: ('y', -1.),
        GLUT_KEY_LEFT: ('y', 1.),
        b'z': ('z', -1.),
        b'a': ('z', 1.)
    }
    __light_keys = {
        b'h': ('x',  .1),
        b'l': ('x', -.1),
        b'j': ('y',  .1),
        b'k': ('y', -.1),
    }

    def __init__(self, model):
        """Initialize input handlers and link given Model to the Input."""
        self.__model = model

        glutKeyboardFunc(lambda key, x, y: self.__handle_key(key, False))
        glutKeyboardUpFunc(lambda key, x, y: self.__handle_key(key, True))
        glutSpecialFunc(lambda key, x, y: self.__handle_special(key, False))
        glutSpecialUpFunc(lambda key, x, y: self.__handle_special(key, True))

    def __handle_special(self, key, release=False):
        """Process special keys of the keyboard."""
        if key in ModelInput.__rotation_keys:
            self.__rotate(ModelInput.__rotation_keys, key, release)
        else:
            return
        self.__model.redraw()

    def __handle_key(self, key, release=False):
        """Process alphanumerical keys of the keyboard."""
        if key in ModelInput.__rotation_keys:
            self.__rotate(ModelInput.__rotation_keys, key, release)
        elif key in ModelInput.__light_keys and not release:
            directed_light = {
                'x': 0.,
                'y': 0.,
                'z': 0.
            }
            axis, value = ModelInput.__light_keys[key]
            directed_light[axis] = value
            self.__model.change_light(direction=directed_light)
        elif key == b'r' and not release:
            self.__model.face = self.__model.generate_face()
            self.__model.redraw()
            return
        elif key == b'q' and not release:
            self.__model.close()
            return
        elif key == b's' and not release:
            t = datetime.now()
            timestamp = int(mktime(t.timetuple()) * 1E6 + t.microsecond)
            self.__model.save_image(join('output', str(timestamp)))
            return
        elif key == b'o' and not release:
            self.__model.optimize()
            return
        else:
            return
        self.__model.redraw()

    def __rotate(self, commands, key, release):
        """Process rotation keys."""
        assert key in commands
        axis, value = commands[key]
        self.__model.rotate(axis, 0. if release else value)
