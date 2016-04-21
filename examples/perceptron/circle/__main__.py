from argparse import ArgumentParser
from random import randint, random

from matplotlib import pyplot as plt
from matplotlib import animation

from classes.solver import Perceptron

parser = ArgumentParser(description='Plane curves recognizer')
parser.add_argument('-R', '--radius',
        type=float, default=random() * 1 + 2,
        help='circle radius')
parser.add_argument('-t', '--interval',
        type=int, default=200,
        help='interval of screen refresh')
args = parser.parse_args()
R = args.radius
interval = args.interval

fig = plt.figure()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

x0 = random() * 5 + 3
y0 = random() * 5 + 3
patch = plt.Circle((x0, y0), R, color='r', fill=False)

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

inside, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
calculated = plt.Circle((0, 0), 0, color='b', fill=False)

perceptron = Perceptron(4)

def Y2X(x, y):
    return (1, x, y, x**2 + y**2)

def init():
    patch.center = (x0, y0)
    ax.add_patch(patch)
    ax.add_patch(calculated)
    return calculated, inside, outside

def animate(i):
    new_x = random() * 10
    new_y = random() * 10

    if (new_x - x0)**2 + (new_y - y0)**2 < R**2 - 1:
        inside_x_points.append(new_x)
        inside_y_points.append(new_y)
        inside.set_data(inside_x_points, inside_y_points)
        perceptron.setup(left=[Y2X(new_x, new_y)])
    elif (new_x - x0)**2 + (new_y - y0)**2 > R**2 + 1:
        outside_x_points.append(new_x)
        outside_y_points.append(new_y)
        outside.set_data(outside_x_points, outside_y_points)
        perceptron.setup(right=[Y2X(new_x, new_y)])

    a = perceptron.alpha
    prediction = {
        'x': -a[1]/(2 * a[3]),
        'y': -a[2]/(2 * a[3]),
    }
    prediction['r'] = abs(a[0]/a[3] - prediction['x']**2 - prediction['y']**2)**.5
    print 'Calculated: x0={}, y0={}, R={}'.format(prediction['x'], prediction['y'], prediction['r'])
    print 'Real: x0={}, y0={}, R={}'.format(x0, y0, R)
    calculated.center = (prediction['x'], prediction['y'])
    calculated.radius = prediction['r']

    return calculated, inside, outside

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=interval,
                               blit=True)

plt.show()

