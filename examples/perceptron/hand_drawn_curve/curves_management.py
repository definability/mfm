from numpy import array, ones

from utils import *
from matrices_management import get_product_matrix


def get_poly(x, order):
    if order == 1:
        return [1]
    elif order == 2:
        return [x, 1]
    return ([1] + [x**i for i in xrange(1, order)])[::-1]


def get_vector(x, y, order):
    return array(get_poly(x, order) + get_poly(y, order))


def get_eq(x, y, A, order):
    v = get_vector(x, y, order)
    return v.dot(A).dot(v)


def get_point_projection(x, y, A, order):
    return get_eq(array([x]), array([y]), A, order)


def get_componentwise_products(v):
    order = v.size
    M = get_product_matrix(ones((order, order)))
    return (v * M * v[:,None]).flatten().tolist()


def get_point_class(point, A, order):
    return sign_treshold(get_point_projection(point[0], point[1], A, order)) 

