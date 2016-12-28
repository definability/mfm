import argparse
import json
import logging

from PIL import Image
from numpy import array

from src import MFM, Model, ModelInput, View, Face
from src.fitter import FittersChain
from data import get_datafile_path


def parse_command_line_arguments():
    LOGGER_LEVELS_COUNT = 6
    LOGGER_LEVELS_STEP = 10
    LOGGER_LEVELS = [logging.getLevelName(i*LOGGER_LEVELS_STEP)
                     for i in range(LOGGER_LEVELS_COUNT)]

    parser = argparse.ArgumentParser(
        description='Morphable Face Model fitting application')
    parser.add_argument(
        '--config', metavar='config', type=str, required=False,
        help='specify configuration file for fitting procedure')
    parser.add_argument('-l', '--log', help='set logger level', type=str.upper,
                        default='WARNING', choices=LOGGER_LEVELS)

    return parser.parse_args()


def setup_logging(level):
    logging.basicConfig(
        level=getattr(logging, level),
        format=' '.join(['[%(asctime)s]', '[%(levelname)8s]',
                         '[%(module)s:%(funcName)s]', '%(message)s']))


def construct_chain(configuration_filename, model):
    fitting_settings = None
    with open(configuration_filename) as config:
        fitting_settings = json.load(config)

    fitters = fitting_settings['fitters']

    face_parameters = fitting_settings['input'].get('initial_face', {})

    coefficients = face_parameters.get('coefficients', [])
    directed_light = face_parameters.get('directed_light', (0., 0., 0.))
    ambient_light = face_parameters.get('ambient_light', 0.)
    initial_face = Face(coefficients=coefficients,
                        directed_light=directed_light,
                        ambient_light=ambient_light)

    face_filename = get_datafile_path(fitting_settings['input']['input_image'])
    image = Image.open(face_filename).convert('L')
    original_data = array(image.getdata()).astype('f') / 255
    image_data = original_data.reshape(image.size)[::-1, :].flatten()
    image.close()

    return FittersChain(fitters, image_data, model, initial_face=initial_face)

def setup_application(configuration_filename=None):
    MFM.init()
    view = View((500, 500))
    model = Model(view)
    ModelInput(model)

    if configuration_filename is None:
        model.start()
    else:
        model.start(construct_chain(configuration_filename, model))

if __name__ == '__main__':
    arguments = parse_command_line_arguments()
    setup_logging(arguments.log)
    setup_application(arguments.config)
