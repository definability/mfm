from matplotlib import pyplot as plt
from matplotlib import animation

from curves_management import *
from perceptron_management import *

def get_canvas(xlim, ylim):
    fig = plt.figure()

    ax = plt.axes(xlim=xlim, ylim=ylim)

    inside, = ax.plot([], [], 'ro')
    outside, = ax.plot([], [], 'bo')

    return fig, ax, inside, outside

def draw_curve(coordinates, A, color, order):
    x, y = coordinates
    plt.contour(x, y[:,None].ravel(),
                get_eq(x, y[:,None], A, order), [0],
                colors=color)

def animate(curve, ax, plots, new_point, point_class):
    inside, outside = plots

    #new_point = curve.generate_point()

    #point_class = get_point_class(new_point, curve.A, curve.order)
    if point_class == -1:
        class_parameters = {
            'x': curve.inside_points[0],
            'y': curve.inside_points[1],
            'plot': inside
        }
    elif point_class == 1:
        class_parameters = {
            'x': curve.outside_points[0],
            'y': curve.outside_points[1],
            'plot': outside
        }
    else:
        return inside, outside

    add_new_point(new_point,
                  class_parameters['x'],
                  class_parameters['y'],
                  class_parameters['plot'],
                  point_class, curve.order, curve.perceptron)


    curve.cache['alpha'] = process_perceptron_output(curve.perceptron,
                                                     curve.cache['alpha'])

    new_A = array(curve.cache['alpha']).reshape(curve.order*2, curve.order*2)
    #draw_curve(curve.grid, curve.A, 'r', curve.order)
    if len(curve.inside_points[0]) > 0 and len(curve.outside_points[0]) > 0:
        plt.gca().clear()
        draw_curve(curve.grid, new_A, 'b', curve.order)
    ax.plot(curve.inside_points[0], curve.inside_points[1], 'ro')
    ax.plot(curve.outside_points[0], curve.outside_points[1], 'bo')
    plt.draw()
    return inside, outside

def run_animation(curve, interval):
    curve.cache = {
        'alpha': None
    }
    fig, ax, inside, outside = get_canvas(curve.x_limits, curve.y_limits)
    #draw_curve(curve.grid, curve.A, 'r', curve.order)
    animate_closure = lambda i: animate(curve, ax, (inside, outside), i)
    #anim = animation.FuncAnimation(fig, animate_closure, interval=interval)
    def onclick(event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
        animate(curve, ax, (inside, outside), (event.xdata, event.ydata), event.button - 2)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

