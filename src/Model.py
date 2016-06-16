from enum import Enum

from OpenGL.GLUT import glutMainLoop
from PIL import Image
from numpy import save, array, column_stack

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

    def save_image(self, filename):
        if self.__texture == Texture.normal:
            img = array(self.__view.get_image())
            img = img.reshape(img.size//4, 4)
            data = column_stack((
                    self.__face.normal_map_to_normal_vectors(img[:, :3]),
                    img[:, 3]))
            with open(filename + '.npy', 'wb') as f:
                save(f, data[::-1])
        elif self.__texture == Texture.light:
            size = self.__view.get_size()
            image = Image.new('RGBA', size)
            data = (self.__view.get_image() * 255).astype('i')
            pixels = [(data[i*4+0], data[i*4+1], data[i*4+2], data[i*4+3])
                       for i in range(size[0]*size[1]-1, -1, -1)]
            image.putdata(pixels)
            image.save(filename + '.png')
            image.close()
            with open(filename + '.light.npy', 'wb') as f:
                light = list(self.__face.get_directed_light())
                light.append(self.__face.get_constant_light())
                save(f, light)
