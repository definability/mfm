from numpy import array, concatenate
from scipy.optimize import minimize

from src import Face
from .ModelFitter import ModelFitter


class NelderMeadFitter(ModelFitter):
    """Fitter which uses Nelder-Mead simplex algorithm."""
    def __init__(self, image, dimensions=199, model=None, offset=1.,
                 initial_face=None, callback=None):
        """
        Offset sets offset for shape parameters from initial face model
        to create simplices.
        """
        super(NelderMeadFitter, self).__init__(image, dimensions, model,
                                               initial_face)
        self.__offset = offset

    def start(self):
        x0 = self._initial_face.as_array.copy()

        final_simplex = x0.copy()
        final_simplex[Face.PCS_SLICE] += self.__offset
        final_simplex[0:-Face.NON_PCS_COUNT:2] = 1
        final_simplex[1:-Face.NON_PCS_COUNT:2] = -1
        final_simplex[Face.NON_PCS_SLICE] = 1

        initial_simplex = array([concatenate((x0[:i], final_simplex[i:]))
                                 for i in range(self._dimensions + 1)], 'f')
        options = {
            'initial_simplex': initial_simplex
        }
        result = minimize(self.get_face_deviation, x0,
                          method='nelder-mead', options=options)
        self.finish(Face.from_array(result))
