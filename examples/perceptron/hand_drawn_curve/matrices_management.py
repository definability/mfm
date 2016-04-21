from numpy import array, ones, zeros, triu, concatenate, column_stack
from numpy.linalg import eigvals, eig

def is_positive_definite(A):
    if A is None:
        return False
    return (eigvals(A) > 0).all()

def get_wrong_vector(A):
    v, w = eig(A)
    return w[:,v<=0][:,0].tolist()

def get_corner_matrix(matrix):
    return triu(matrix)[::-1]

def get_product_matrix(matrix):
    size = matrix.shape[0] / 2
    left_top = matrix[:size,:size]
    left_bottom = matrix[:size,size:]
    right_top = matrix[size:,:size]
    right_bottom = matrix[size:,size:]
    a = concatenate((zeros((size, size)), get_corner_matrix(left_bottom)))
    b = concatenate((get_corner_matrix(right_top), zeros((size, size))))
    return column_stack((a, b))

