from argparse import ArgumentParser
from random import randint, random

from matplotlib import pyplot as plt
from matplotlib import animation

from classes.solver import Perceptron
from examples.perceptron.points_radius.find_wrong import get_correction_point

parser = ArgumentParser(description='Plane curves recognizer')
parser.add_argument('-R', '--radius',
        type=float, default=random() * .5 + 1.2,
        help='radius of circles')
parser.add_argument('-t', '--interval',
        type=int, default=200,
        help='interval of screen refresh')
args = parser.parse_args()
R = args.radius
interval = args.interval

fig = plt.figure()

LEFT_X = -10
RIGHT_X = 10
X = [-10, 10]

LEFT_Y = -10
RIGHT_Y = 10
DEFAULT_Y = [0, 0]

ax = plt.axes(xlim=(LEFT_X, RIGHT_X), ylim=(LEFT_Y, RIGHT_Y))

R_MUL = 1.1
a = (random() - .5) * 5
b = (random() - .5) * 5
c = (random() - .5) * 5
k = (a**2 + b**2 + c**2) ** .5
a /= k
b /= k
c /= k

def get_y(a, b, c, x):
    return - (x[0] * a + c) / b, - (x[1] * a + c) / b

inside_x_points = []
inside_y_points = []
inside_x_points_corrections = []
inside_y_points_corrections = []

outside_x_points = []
outside_y_points = []
outside_x_points_corrections = []
outside_y_points_corrections = []

inside, = ax.plot([], [], 'ro')
inside_corrections, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
outside_corrections, = ax.plot([], [], 'bo')
lines, = ax.plot(X, get_y(a, b, c, X), 'r')
calculated, = ax.plot(X, DEFAULT_Y, 'b')

perceptron = Perceptron(3)

def Y2X(x, y):
    return (1, x, y)

def init():
    return inside, outside, lines, inside_corrections, outside_corrections

def animate(i):

    alpha = perceptron.alpha
    a_k = sum(c**2 for c in alpha) ** .5
    n = len(inside_x_points)
    need_correction = True and a_k > 0 and n > 0
    corrected = False
    while need_correction:
        alpha = perceptron.alpha
        points = zip(inside_x_points, inside_y_points) + \
                 zip(outside_x_points, outside_y_points)
        correction = get_correction_point(alpha, R, points)
        if correction is None:
            need_correction = False
            break

        new_x = correction[1]
        new_y = correction[2]

        if new_x * a + new_y * b + c < 0:
            inside_x_points_corrections.append(new_x)
            inside_y_points_corrections.append(new_y)
            inside_corrections.set_data(inside_x_points_corrections,
                                        inside_y_points_corrections)
            perceptron.setup(left=[Y2X(new_x, new_y)])
            print 'Corrected left', correction[1:]
        if new_x * a + new_y * b + c > 0:
            outside_x_points_corrections.append(new_x)
            outside_y_points_corrections.append(new_y)
            outside_corrections.set_data(outside_x_points_corrections,
                                         outside_y_points_corrections)
            perceptron.setup(right=[Y2X(new_x, new_y)])
            print 'Corrected right', correction[1:]
        corrected = True

    if not corrected:
        new_x = (random() - .5) * 20
        new_y = (random() - .5) * 20

        if new_x * a + new_y * b + c < - R_MUL * R:
            inside_x_points.append(new_x)
            inside_y_points.append(new_y)
            inside.set_data(inside_x_points, inside_y_points)
            patch = plt.Circle((new_x, new_y), R, color='r', fill=False)
            ax.add_patch(patch)
            perceptron.setup(left=[Y2X(new_x, new_y)])
        if new_x * a + new_y * b + c > R_MUL * R:
            outside_x_points.append(new_x)
            outside_y_points.append(new_y)
            outside.set_data(outside_x_points, outside_y_points)
            patch = plt.Circle((new_x, new_y), R, color='b', fill=False)
            ax.add_patch(patch)
            perceptron.setup(right=[Y2X(new_x, new_y)])

    a_k = a_k if a_k > 0 else 1
    prediction = {
        'c': alpha[0]/a_k,
        'a': alpha[1]/a_k,
        'b': alpha[2]/a_k
    }
    #print 'Calculated: a={}, b={}, c={}'.format(prediction['a'], prediction['b'], prediction['c'])
    #print 'Real: a={}, b={}, c={}'.format(a, b, c)
    try:
        y = get_y(prediction['a'], prediction['b'], prediction['c'], X)
    except:
        y = DEFAULT_Y
    calculated.set_data(X, y)

    return inside, outside, calculated, inside_corrections, outside_corrections

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=interval,
                               blit=False)

plt.show()

