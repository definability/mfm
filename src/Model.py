"""Model of the MVC application."""
from PIL import Image
from numpy import save, array

from src import MFM


def safe_add(direction, direction_delta, check_constraints=False):
    """Check resulting vector values and add if not violates constraints.

    Constraints are [-1; 1].
    """
    x, y, z = direction
    new_x = x + direction_delta['x']
    new_y = y + direction_delta['y']
    new_z = z + direction_delta['z']
    if not check_constraints or (-1 <= new_x <= 1 and -1 <= new_y <= 1):
        return new_x, new_y, new_z
    return direction


class Model(object):
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

        self.__rotations = {
            'x': 0.,
            'y': 0.,
            'z': 0.
        }

        self.face = self.generate_face()

    @property
    def face(self):
        """Get current Face."""
        return self.__face

    @face.setter
    def face(self, face):
        """Set current Face."""
        self.__face = face
        self.__view.face = face

    def start(self, fitter=None):
        """Start main application loop."""
        self.__fitter = fitter
        self.__view.start()

    def redraw(self, callback=None):
        """Trigger rendering procedure."""
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
            self.face = face
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__on_draw_callbacks.append((face, callback))

    def get_image(self, face):
        self.face = face
        self.__view.redraw(synchronous=True)
        img = array(self.__view.get_image())
        img = img.reshape(img.size//4, 4)
        return img

    def __on_redraw(self, callback):
        img = array(self.__view.get_image())
        img = img.reshape(img.size//4, 4)
        callback(img)
        if len(self.__on_draw_callbacks) > 0:
            face, callback = self.__on_draw_callbacks.pop(0)
            self.face = face
            self.redraw(lambda: self.__on_redraw(callback))
        else:
            self.__now_processing = False

    @staticmethod
    def generate_face():
        """Get new random Face instance."""
        return MFM.get_face()

    def rotate(self, direction=None, check_constraints=False):
        """Rotate camera of the viewport.

        Adds (not sets) rotation value for given axis.
        """
        if direction is not None:
            self.__face.position = safe_add(self.__face.position, direction,
                                            check_constraints)

    def change_light(self, direction=None, intensity=None,
                     check_constraints=False):
        """Change light parameters.

        Set vector for directed light and intensity for ambient light.
        """
        if direction is not None:
            self.__face.directed_light = safe_add(self.__face.directed_light,
                                                  direction, check_constraints)
        if intensity is not None:
            self.__face.ambient_light += intensity

    def close(self):
        """Close the viewport"""
        self.__view.close()

    def optimize(self):
        """Start the fitting procedure."""
        if self.__fitter is not None:
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
