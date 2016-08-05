from enum import Enum
from warnings import warn

from OpenGL.GLUT import glutMainLoop
from PIL import Image
from numpy import save, array, column_stack, concatenate, apply_along_axis
import numpy

from src import MFM


class Texture(Enum):
    """Enumerate of Face textures.

    Face can be displayed in two modes:
    - shadow map;
    - normal map.
    """
    light = 0
    normal = 1


class Model:
    """Main processor of the application.

    Makes calculations for Faces, works with Fitters and requests
    View to render.
    """
    def __init__(self, view):
        """Create model with given View.

        Creates initial light and rotation conditions and renders first Face.
        """
        self.__light = True
        self.__face = None
        self.__view = view
        self.__fitter = None
        self.__on_draw_callbacks = []
        self.__now_processing = False

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

    def start(self, fitter):
        """Start main application loop."""
        self.__fitter = fitter
        glutMainLoop()

    def redraw(self, callback=None):
        """Trigger rendering procedure."""
        # print('redrawing')
        self.__view.redraw(callback)

    def request_normals(self, coefficients, callback):
        """Send request for normal vectors with coefficients.

        Adds callback with given coefficients to queue and starts
        calculation and rendering procedure.

        Handy for fitting procedure:
        - Fitter requests normal vectors with provided Face parameters
        and sends callback function;
        - Model renders Face with given parameters and sends achived
        normal vectors via callback.
        """
        warn('Normal map is deprecated. Use request_image instead',
             DeprecationWarning)
        if self.__texture == Texture.light:
            self.toggle_texture()

        if len(self.__on_draw_callbacks) == 0 and not self.__now_processing:
            self.__now_processing = True
            self.calculate(True, coefficients)
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__on_draw_callbacks.append((coefficients, callback))

    def request_image(self, face, callback):
        """Send request for rendered face with given parameters.

        Adds callback with given face to queue and starts
        calculation and rendering procedure.

        Handy for fitting procedure:
        - Fitter requests rendered face with provided Face parameters
          and sends callback function;
        - Model renders Face with given parameters and sends achived
          image via callback.
        """
        if self.__texture == Texture.normal:
            self.toggle_texture()

        if len(self.__on_draw_callbacks) == 0 and not self.__now_processing:
            self.__now_processing = True
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__on_draw_callbacks.append((face, callback))

    def __on_redraw(self, callback):
        # print('redraw callback')
        img = array(self.__view.get_image())
        img = img.reshape(img.size//4, 4)
        data = column_stack((
            self.__face.normal_map_to_normal_vectors(img[:, :3]), img[:, 3]))
        callback(data)
        if len(self.__on_draw_callbacks) > 0:
            coefficients, callback = self.__on_draw_callbacks.pop(0)
            self.calculate(True, coefficients)
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__now_processing = False

    def calculate(self, new_model=True, coefficients=None):
        """Generates new face or changes light of old face.

        If `new_model` is `True`
        - if `coefficients` is a tuple of numbers, new Face will be generated
        on the base of old one, but coefficient `coefficients[0]`
        will be changed to `coefficients[1]`;
        - in other case new random Face will be generated.
        """
        warn('Shaders will make all calculations', DeprecationWarning)
        if new_model and type(coefficients) is not tuple:
            self.__face = MFM.get_face(coefficients)
        elif new_model:
            self.__face = MFM.change_coefficient(
                self.__face, coefficients[0], coefficients[1])

        self.__view.vertices = self.__face.get_vertices()

        normals = self.__view.normals = self.__face.get_normals()

        normal_min = apply_along_axis(numpy.min, 0, normals)
        normal_max = apply_along_axis(numpy.max, 0, normals)

        self.__face.normal_min = normal_min
        self.__face.normal_max = normal_max

        if self.__texture is Texture.normal:
            self.__view.light = concatenate((
                concatenate((normal_min, [-1])),
                concatenate((normal_max - normal_min, [1])),
                [0] * 4))
        elif self.__texture is Texture.light:
            self.__view.light = concatenate((self.__face.light, [0] * 8))

    def rotate(self, axis, value):
        """Rotate camera of the viewport.

        Adds (not sets) rotation value for given axis.
        """
        self.__rotations[axis] = value
        rotation = (self.__rotations['x'], self.__rotations['y'],
                    self.__rotations['z'])
        self.__view.rotation = rotation

    def change_light(self, direction=None, intensity=None):
        """Change light parameters.

        Set vector for directed light and intensity for ambient light.
        """
        warn('Shaders will make all calculations', DeprecationWarning)
        if direction is not None:
            x, y, z = self.__face.get_directed_light()
            self.__face.set_light(
                directed_light=(x + direction['x'], y + direction['y'],
                                z + direction['z']))
        if intensity is not None:
            constant_light = self.__face.get_constant_light()
            constant_light += intensity
            self.__face.set_light(constant_light=constant_light)
        self.calculate(False)

    def toggle_texture(self):
        """Toggle Face texture between shadow and normal map."""
        if self.__texture == Texture.light:
            warn('Normal map texture is deprecated', DeprecationWarning)
            self.__texture = Texture.normal
        else:
            self.__texture = Texture.light

    def close(self):
        """Close the viewport"""
        self.__view.close()

    def optimize(self):
        """Start the fitting procedure."""
        self.__fitter.start()

    def save_image(self, filename):
        """Render current viewport state to file.

        If normal map used, result will be saved to NumPy file.
        File will contain matrix, where each cell will match image pixel
        and contain normal vector.

        If shadow map used, result will be simply rendered.
        Also light conditions will be saved to NumPy file.
        """
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
                light = list(self.__face.directed_light)
                light.append(self.__face.ambient_light)
                save(f, light)
