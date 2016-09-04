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
