from .ModelFitter import ModelFitter

import src.fitter


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

    fitter = self.__fitters.pop(0)
    parameters = self.__parameters.pop(0)

    callback = final_callback
    parameters['callback'] = final_callback
    if len(self.__fitters) > 1:
        tail_fitters = fitter[:]
        tail_parameters = parameters[:]
        parameters['callback'] = lambda face: make_chain(
            tail_fitters, tail_parameters, final_callback, face)

    parameters['initial_face'] = initial_face

    return fitter(**parameters)


class FittersChain:
    """Class for Face fitters chaining."""
    def __init__(self, chain, image, model, dimensions=199):
        """Build chain of Fitters."""
        self.__parameters = []
        self.__fitters = []
        for node in chain:
            self.__parameters.append(
                {key: value for key, value in node.items() if key != 'fitter'})
            self.__fitters.append(parse_fitter(node['fitter']))
        for key in self.__parameters:
            self.__parameters[key]['image'] = image
            self.__parameters[key]['model'] = model

    def start(self, callback):
        """Start fitting procedure."""
        raise NotImplementedError()
