from numpy import array, nonzero
from numpy.linalg import lstsq, norm


class ModelFitter:
    def __init__(self, image):
        self.__image = image

    def check(self, normals):
        indices = nonzero(normals[:, 3])

        N = normals[indices]
        Y = self.__image[indices]

        N_x = N[:, 0]
        N_y = N[:, 1]
        N_z = N[:, 2]

        y_x = Y.dot(N_x)
        y_y = Y.dot(N_y)
        y_z = Y.dot(N_z)

        n_x = N_x.sum()
        n_y = N_y.sum()
        n_z = N_z.sum()

        n_xx = N_x.dot(N_x)
        n_xy = N_x.dot(N_y)
        n_xz = N_x.dot(N_z)
        n_yy = N_y.dot(N_y)
        n_yz = N_y.dot(N_z)
        n_zz = N_z.dot(N_z)

        A = array([
            [n_xx, n_xy, n_xz, n_x   ],
            [n_xy, n_yy, n_yz, n_y   ],
            [n_xz, n_yz, n_zz, n_z   ],
            [n_x,  n_y,  n_z,  len(N)]
        ])
        y = array([y_x, y_y, y_z, Y.sum()])

        x, _, _, _ = lstsq(A, y)

        return x
