from enum import Enum

from OpenGL.GLUT import glutMainLoop

from src import MFM, View


class Texture(Enum):
    light = 0
    normal = 1


class Model:
    def __init__(self):
        self.__light = True
        self.__face = None
        self.__view = View((500, 500))

        self.__texture = Texture.light

        self.__rotations = {
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

    def toggle_texture(self):
        self.__texture = Texture.normal if self.__texture == Texture.light \
                    else Texture.light

    def close(self):
        self.__view.close()
