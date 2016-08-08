from warnings import warn

from numpy import array, nonzero, zeros
from numpy.linalg import lstsq  # , inv


class ModelFitter:
    """Abstract class for Face fitting procedure.

    Should call Face rendering and wait for response.
    """
    def __init__(self, image, dimensions=199, model=None, initial=None,
                 initial_face=None):
        """Initializes fitter for given image.

        Fits provided number of dimensions of given model to the image.
        """
        self.__image = array(image)
        self.__model = model
        self._dimensions = dimensions

        self._initial = initial
        if self._initial is None:
            warn('Use initial_face instead of initial coefficients',
                 DeprecationWarning)
            self._initial = zeros(self._dimensions, dtype='f')
        else:
            self._initial_face = initial_face

    def estimate_light(self, normals):
        """Estimates light parameters to the image with given normal vectors.

        Light parameters contain vector of directed light
        and intensity of ambient light.
        """
        warn('New shadows model', DeprecationWarning)
        indices = nonzero(normals[:, 3])

        N = normals[indices]
        Y = self.__image[indices]

        N_x = N[:, 0]
        N_y = N[:, 1]
        N_z = N[:, 2]

        y_x = Y.dot(N_x)
        y_y = Y.dot(N_y)
        y_z = Y.dot(N_z)

        n_x = N_x.sum()
        n_y = N_y.sum()
        n_z = N_z.sum()

        n_xx = N_x.dot(N_x)
        n_xy = N_x.dot(N_y)
        n_xz = N_x.dot(N_z)
        n_yy = N_y.dot(N_y)
        n_yz = N_y.dot(N_z)
        n_zz = N_z.dot(N_z)

        A = array([
            [n_xx, n_xy, n_xz, n_x],
            [n_xy, n_yy, n_yz, n_y],
            [n_xz, n_yz, n_zz, n_z],
            [n_x, n_y, n_z, len(N)]
        ])
        y = array([y_x, y_y, y_z, Y.sum()])

        x, _, _, _ = lstsq(A, y)
        # Fails `test_estimate_light` test, because matrix cannot be inverted.
        # x = inv(A).dot(y)

        return x

    def start(self):
        """Start fitting procedure.

        Should be called by host.
        """
        raise NotImplementedError()

    def request_normals(self, parameters, index=None):
        """Requests normals from Model with given parameters.

        Parameter `index` is a label for the request.
        Will be provided with callback for Fitter to identify
        request, which provoked this response.
        """
        warn('New shadows model', DeprecationWarning)
        self.__model.request_normals(
            parameters, lambda normals: self.receive_normals(normals, index))

    def request_face(self, face, label=None):
        """Requests rendered face with given parameters.

        Label will be provided with callback for Fitter to identify
        request, which provoked this response.
        """
        self.__model.request_face(
            face, lambda image: self.receive_image(image, label))

    def receive_normals(self, normals, index=None):
        """Callback for host on render.

        Provides normal vectors and label, with which Face was requested.
        """
        raise NotImplementedError()

    def receive_image(self, image, index=None):
        """Callback for host on renderer.

        Provides normal vectors and label of Face which was requested.
        """
        raise NotImplementedError()

    def get_image_deviation(self, image, normals):
        """Cost function for fitting result."""
        diff = image - self.__image
        indices = nonzero(normals[:, 3])
        return (diff[indices] ** 2).mean()
