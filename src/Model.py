from enum import Enum

from OpenGL.GLUT import glutMainLoop

from src import MFM


class Texture(Enum):
    light = 0
    normal = 1


class Model:
    def __init__(self, view):
        self.__light = True
        self.__face = None
        self.__view = view

        self.__texture = Texture.light

        self.__rotations = {
            'x': 0.,
            'y': 0.,
            'z': 0.
        }
        self.__light = {
            'x': 0.,
            'y': 0.,
            'z': 0.
        }

        self.calculate()

    def start(self):
        glutMainLoop()

    def redraw(self):
        self.__view.redraw()

    def calculate(self, new_model=True):
        if new_model:
            self.__face = MFM.get_face()

        vertices = self.__face.get_vertices_c()
        if self.__texture == Texture.light:
            colors = self.__face.get_light_map_c()
        else:
            colors = self.__face.get_normal_map_c()

        self.__view.update(vertices, colors)

    def rotate(self, axis, value):
        self.__rotations[axis] = value
        rotation = (self.__rotations['x'], self.__rotations['y'],
                    self.__rotations['z'])
        self.__view.update(rotation=rotation)

    def change_light(self, direction=None, intensity=None):
        if direction is not None:
            x, y, z = self.__face.get_directed_light()
            self.__face.set_light(directed_light=(x + direction['x'],
                                  y + direction['y'], z + direction['z']))
        if intensity is not None:
            constant_light = self.__face.get_constant_light()
            constant_light += intensity
            self.__face.set_light(constant_light=constant_light)
        self.calculate(False)

    def toggle_texture(self):
        self.__texture = Texture.normal if self.__texture == Texture.light \
                    else Texture.light

    def close(self):
        self.__view.close()
