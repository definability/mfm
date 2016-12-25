from enum import Enum

from OpenGL.GLUT import glutMainLoop
from PIL import Image
from numpy import save, array

from src import MFM


class Texture(Enum):
    """Enumerate of Face textures.

    Face can be displayed in single mode:
    - shadow map;
    """
    light = 0


class Model:
    """Main processor of the application.

    Makes calculations for Faces, works with Fitters and requests
    View to render.
    """
    def __init__(self, view):
        """Create model with given View.

        Creates initial light and rotation conditions and renders first Face.
        """
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

        self.face = self.generate_face()

    @property
    def face(self):
        return self.__face

    @face.setter
    def face(self, face):
        self.__face = face
        self.__view.face = face

    def start(self, fitter):
        """Start main application loop."""
        self.__fitter = fitter
        glutMainLoop()

    def redraw(self, callback=None):
        """Trigger rendering procedure."""
        # print('redrawing')
        self.__view.redraw(callback)

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
        if len(self.__on_draw_callbacks) == 0 and not self.__now_processing:
            self.__now_processing = True
            self.__view.face = face
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__on_draw_callbacks.append((face, callback))

    def __on_redraw(self, callback):
        # print('redraw callback')
        img = array(self.__view.get_image())
        img = img.reshape(img.size//4, 4)
        callback(img)
        if len(self.__on_draw_callbacks) > 0:
            face, callback = self.__on_draw_callbacks.pop(0)
            self.__view.face = face
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__now_processing = False

    def generate_face(self):
        return MFM.get_face()

    def rotate(self, axis, value):
        """Rotate camera of the viewport.

        Adds (not sets) rotation value for given axis.
        """
        if direction is not None:
            x, y, z = self.__face.position
            self.__face.position = (
                x + direction['x'],
                y + direction['y'],
                z + direction['z'])

    def change_light(self, direction=None, intensity=None):
        """Change light parameters.

        Set vector for directed light and intensity for ambient light.
        """
        if direction is not None:
            x, y, z = self.__face.directed_light
            self.__face.directed_light = (
                x + direction['x'],
                y + direction['y'],
                z + direction['z'])
        if intensity is not None:
            constant_light = self.__face.get_constant_light()
            constant_light += intensity
            self.__face.ambient_light = constant_light

    def close(self):
        """Close the viewport"""
        self.__view.close()

    def optimize(self):
        """Start the fitting procedure."""
        self.__fitter.start()

    def save_image(self, filename):
        """Render current viewport state to file.

        If shadow map used, result will be simply rendered.
        Also light conditions will be saved to NumPy file.
        """
        size = self.__view.get_size()
        image = Image.new('RGBA', size)
        data = (self.__view.get_image() * 255).astype('i')
        data = data.reshape(size[1], size[0], 4)[::-1, :, :].flatten()
        pixels = [tuple(data[i*4:i*4+4]) for i in range(size[0]*size[1])]
        image.putdata(pixels)
        image.save(filename + '.png')
        image.close()
        with open(filename + '.array.npy', 'wb') as f:
            save(f, self.__face.as_array)
