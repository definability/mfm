from curves_management import *

def add_new_point(point, x_list, y_list, plot, side, order, perceptron):
    x_list.append(point[0])
    y_list.append(point[1])
    plot.set_data(x_list, y_list)
    points = get_componentwise_products(get_vector(point[0], point[1], order))
    if side == -1:
        perceptron.setup(left=[points])
    if side == 1:
        perceptron.setup(right=[points])


def process_perceptron_output(perceptron, previous_data):
    try:
        data = perceptron.alpha
    except:
        return previous_data
    if previous_data == data:
        return previous_data
    print 'Calculated data={}'.format(data)
    #print 'Real data={}'.format(A)
    return data

