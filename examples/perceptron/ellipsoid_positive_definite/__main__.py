from random import randint, random
from math import pi, sin, cos

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse

from classes.solver import Perceptron
from examples.perceptron.ellipsoid_positive_definite.ellipsoid_calculations import Y2X_ellipsoid, get_ellipse
from examples.perceptron.ellipsoid_positive_definite.matrix_calculations import is_positive_definite


X0 = 0
Y0 = 0

LEFT_X = -1
RIGHT_X = 1
LIMITS_X = (LEFT_X, RIGHT_X)

UPPER_Y = 1
BOTTOM_Y = -1
LIMITS_Y = (BOTTOM_Y, UPPER_Y)

fig = plt.figure()

ax = plt.axes(xlim=LIMITS_X, ylim=LIMITS_Y)

a = (random() * 2 + 1) / 4
b = (random() * 2 + 1) / 4
x0 = X0
y0 = Y0
angle = (random() - 0.5) * 2 * pi
w = 2 * a
h = 2 * b

patch = Ellipse((x0, y0), w, h, angle=180*angle/pi, color='r', fill=False)

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

inside, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
calculated = Ellipse((0, 0), 0, 0, color='b', fill=False)
            
perceptron = Perceptron(5)


def init():
    ax.add_patch(patch)
    ax.add_patch(calculated)
    return calculated, inside, outside


def get_point_projection(new_x, new_y):
    r1 = (new_x * cos(angle) + new_y * sin(angle)) / a
    r2 = (new_x * sin(angle) - new_y * cos(angle)) / b
    return r1**2 + r2**2


def get_point_class(new_x, new_y):
    treshold = .3
    prj = get_point_projection(new_x, new_y)
    if prj < 1 - treshold:
        return -1
    if prj > 1 + treshold:
        return 1
    return 0


def add_new_point(new_x, new_y, x_list, y_list, plot, side):
    x_list.append(new_x)
    y_list.append(new_y)
    plot.set_data(x_list, y_list)
    if side == -1:
        perceptron.setup(left=[Y2X_ellipsoid(new_x, new_y)])
    if side == 1:
        perceptron.setup(right=[Y2X_ellipsoid(new_x, new_y)])

def process_perceptron_output(previous_data):
    try:
        data = get_ellipse(perceptron.alpha)
    except:
        return previous_data
    if previous_data == data:
        return previous_data
    print 'Calculated: a={}, b={}, angle={}'.format(*data)
    print 'Real: a={}, b={}, angle={}'.format(a, b, angle)
    print 'Positive definite:', is_positive_definite(perceptron.alpha)
    calculated.center = (X0, Y0)
    calculated.width = 2 * data[0]
    calculated.height = 2 * data[1]
    calculated.angle = 180 * data[2] / pi
    return data


perceptron_output = {
    'data': (0, 0, 0)
}
def animate(i):
    new_x = (random() - .5) * 2
    new_y = (random() - .5) * 2

    point_class = get_point_class(new_x, new_y)
    if point_class == -1:
        add_new_point(new_x, new_y, inside_x_points, inside_y_points, inside, -1)
    elif point_class == 1:
        add_new_point(new_x, new_y, outside_x_points, outside_y_points, outside, 1)
    else:
        return calculated, inside, outside
    perceptron_output['data'] = process_perceptron_output(perceptron_output['data'])

    return calculated, inside, outside

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=2000,
                               blit=True)

plt.show()

