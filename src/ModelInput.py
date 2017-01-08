from time import mktime
from datetime import datetime
from os.path import join

from OpenGL.GLUT import GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLUT import GLUT_KEY_DOWN, GLUT_KEY_UP

from OpenGL.GLUT import glutSpecialFunc, glutKeyboardUpFunc, glutKeyboardFunc


class ModelInput:
    """Process input and trigger needed methods of Model."""
    __rotation_keys = {
        GLUT_KEY_UP:    ('y', .1),
        GLUT_KEY_DOWN:  ('y', -.1),
        GLUT_KEY_RIGHT: ('x', -.1),
        GLUT_KEY_LEFT:  ('x', .1),
        b'z':           ('z', -.1),
        b'a':           ('z', .1)
    }
    __light_keys = {
        b'h': ('x', .1),
        b'l': ('x', -.1),
        b'j': ('y', .1),
        b'k': ('y', -.1),
    }

    def __init__(self, model):
        """Initialize input handlers and link given Model to the Input."""
        self.__model = model

        glutKeyboardFunc(lambda key, x, y: self.__handle_key(key, False))
        glutKeyboardUpFunc(lambda key, x, y: self.__handle_key(key, True))
        glutSpecialFunc(lambda key, x, y: self.__handle_special(key))

    def __get_initial_rotation(self):
        return {
            'x': 0.,
            'y': 0.,
            'z': 0.
        }

    def __handle_special(self, key):
        """Process special keys of the keyboard."""
        if key in ModelInput.__rotation_keys:
            position = self.__get_initial_rotation()
            axis, value = ModelInput.__rotation_keys[key]
            position[axis] = value
            self.__model.rotate(direction=position, check_constraints=True)
        else:
            return
        self.__model.redraw()

    def __handle_key(self, key, release=False):
        """Process alphanumerical keys of the keyboard."""
        if release:
            return
        need_redraw = False
        need_redraw |= self.__handle_alphanumerical_move(key, release)
        need_redraw |= self.__handle_application_control(key, release)
        if need_redraw:
            self.__model.redraw()

    def __handle_alphanumerical_move(self, key, release=False):
        if key in ModelInput.__rotation_keys:
            position = self.__get_initial_rotation()
            axis, value = ModelInput.__rotation_keys[key]
            position[axis] = value
            self.__model.rotate(direction=position, check_constraints=True)
            return True
        elif key in ModelInput.__light_keys and not release:
            directed_light = self.__get_initial_rotation()
            axis, value = ModelInput.__light_keys[key]
            directed_light[axis] = value
            self.__model.change_light(direction=directed_light,
                                      check_constraints=True)
            return True
        return False

    def __handle_application_control(self, key, release=False):
        if release:
            return False
        elif key == b'r':
            self.__model.face = self.__model.generate_face()
            self.__model.redraw()
            return True
        elif key == b'q':
            self.__model.close()
            return False
        elif key == b's':
            t = datetime.now()
            timestamp = int(mktime(t.timetuple()) * 1E6 + t.microsecond)
            self.__model.save_image(join('output', str(timestamp)))
            return False
        elif key == b'o':
            self.__model.optimize()
            return False
        return False
