from argparse import ArgumentParser, ArgumentTypeError

from numpy import array, linspace, ones
from numpy.random import rand as random_matrix

from classes.solver import Perceptron
from draw import run_animation
from matrices_management import *
from CurveExample import CurveExample

SCALE = 1

LEFT_X = -1 * SCALE
RIGHT_X = 1 * SCALE
LIMITS_X = (LEFT_X, RIGHT_X)

UPPER_Y = 1 * SCALE
BOTTOM_Y = -1 * SCALE
LIMITS_Y = (BOTTOM_Y, UPPER_Y)

RESOLUTION = 100

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

def check_positive_integer(value):
    order = int(value)
    if order <= 0:
        message = "{} is not a positive integer".format(value)
        raise ArgumentTypeError(message)
    return order

if __name__ == '__main__':
    parser = ArgumentParser(description='Plane curves recognizer')
    parser.add_argument('-n', '--order',
            type=check_positive_integer, default=2,
            help='order of curve to recognize')
    parser.add_argument('-t', '--interval',
            type=check_positive_integer, default=200,
            help='interval of screen refresh')
    args = parser.parse_args()
    order = args.order + 1
    interval = args.interval
    #A = None
    #while not is_positive_definite(A):
    #    A = get_product_matrix(random_matrix(order*2, order*2) - .5)
    A = get_product_matrix(random_matrix(order*2, order*2) - .5)
    print 'Parameters:', A

    perceptron = Perceptron((order*2)**2)

    curve = CurveExample(perceptron, A,
                (inside_x_points, inside_y_points),
                (outside_x_points, outside_y_points),
                order, LIMITS_X, LIMITS_Y, RESOLUTION)
    run_animation(curve, interval)

