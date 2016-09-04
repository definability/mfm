import src.fitter

from .ModelFitter import ModelFitter

def parse_fitter(fitter):
    """Get Fitter class from input parameter."""
    if isinstance(fitter, ModelFitter):
        return fitter
    elif fitter in src.fitter.__all__:
        return src.fitter.__dict__[fitter]
    elif fitter + 'Fitter' in src.fitter.__all__:
        return src.fitter.__dict__[fitter + 'Fitter']
    raise ValueError('{} is not a valid fitter'.format(fitter))


def make_chain(initial_face, fitters, parameters, final_callback):
    """Make chain of fitters.

    Returns first fitter of the chain.
    """
    if len(fitters) == 0:
        return

    callback = final_callback
    if len(fitters) > 1:
        tail_fitters = fitters[1:]
        tail_parameters = parameters[1:]
        callback = lambda face: make_chain(
            face, tail_fitters, tail_parameters, final_callback).start()

    fitter = fitters[0]
    parameters = parameters[0]
    parameters['callback'] = callback
    parameters['initial_face'] = initial_face

    return fitter(**parameters)


class FittersChain:
    """Class for Face fitters chaining."""
    def __init__(self, chain, image, model,
                 initial_face=None, callback=None):
        """Build chain of Fitters."""
        self.__parameters = []
        self.__fitters = []
        self.__initial_face = initial_face
        self.__callback = callback

        common_parameters = {
            'image': image,
            'model': model
        }
        for node in chain:
            parameters = {key: value
                          for key, value in node.items()
                          if key != 'fitter'}
            parameters.update(common_parameters)
            self.__parameters.append(parameters)
            self.__fitters.append(parse_fitter(node['fitter']))

        self.__chain = make_chain(
            self.__initial_face, self.__fitters, self.__parameters,
            self.__callback)

    def start(self):
        """Start fitting procedure."""
        self.__chain.start()
