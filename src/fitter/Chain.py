from .ModelFitter import ModelFitter

import src.fitter


class FittersChain:
    """Class for Face fitters chaining."""
    def __init__(self, chain, image, model, dimensions=199):
        """Build chain of Fitters."""
        self.__parameters = []
        self.__fitters = []
        for node in chain:
            self.__parameters.append(
                {key: value for key, value in node.items() if key != 'fitter'})
            self.__fitters.append(FittersChain.parse_fitter(node['fitter']))

    def start(self, callback):
        """Start fitting procedure."""
        raise NotImplementedError()

    @staticmethod
    def parse_fitter(fitter):
        """Get Fitter class from input parameter."""
        if isinstance(fitter, ModelFitter):
            return fitter
        elif fitter in src.fitter.__all__:
            return src.fitter.__dict__[fitter]
        elif fitter + 'Fitter' in src.fitter.__all__:
            return src.fitter.__dict__[fitter + 'Fitter']
        raise NotImplementedError()
