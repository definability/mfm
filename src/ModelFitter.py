from PIL import Image
from numpy import array, nonzero, mean, zeros, ones, argsort, column_stack
from numpy.random import randn
from numpy.linalg import lstsq, norm  # , inv


class ModelFitter:
    def __init__(self, image, dimensions=199, model=None):
        self.__image = array(image)
        self.__model = model
        self.__dimensions = dimensions

        self.__step = None
        self.__parameters = [None] * (self.__dimensions)
        self.__errors = [None] * (self.__dimensions)
        self.__normals = None

        self.__centroid = None
        self.__reflection = None
        self.reflection_error = None
        self.__expansion = None
        self.expansion_error = None
        self.__contraction = None
        self.contraction_error = None
        self.__end = None
        self.end_error = None

        self.__alpha = 1.
        self.__gamma = 2.
        self.__rho = .5
        self.__sigma = .5

    def estimate_light(self, normals):
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
            [n_xx, n_xy, n_xz, n_x],
            [n_xy, n_yy, n_yz, n_y],
            [n_xz, n_yz, n_zz, n_z],
            [n_x,  n_y,  n_z, len(N)]
        ])
        y = array([y_x, y_y, y_z, Y.sum()])

        x, _, _, _ = lstsq(A, y)
        # TODO: why does this fail `test_estimate_light` test?
        # x = inv(A).dot(y)

        return x

    def start(self):
        self.__initiate_parameters()

    def __request_normals(self, parameters, index=None):
        # # print('requested normals')
        self.__model.request_normals(parameters,
            lambda normals: self.receive_normals(normals, index))

    def __initiate_parameters(self):
        self.__step = 'start'
        for i in range(self.__dimensions):
            # print('Initial step {} of {}'.format(i, self.__dimensions))
            self.__parameters[i] = randn(self.__dimensions) * 1
            # self.__parameters[i] = zeros(self.__dimensions)
            # self.__parameters[i][:i] = 1.
            self.__request_normals(self.__parameters[i], i)
        # self.__end = ones(self.__dimensions)
        self.__end = randn(self.__dimensions)
        self.__request_normals(self.__end, self.__dimensions)

    def receive_normals(self, normals, index=None):
        light = self.estimate_light(normals)
        error = ((normals.dot(light) - self.__image) ** 2).sum()
        self.__normals = normals
        self.__light = light
        # print('Received normals for step', self.__step, 'with error', error)

        if self.__step in ['reflection', 'expansion', 'contraction']:
            setattr(self, self.__step + '_error', error)
            getattr(self, 'calculate_' + getattr(self, self.__step)())()

        elif self.__step == 'shrink' and index == self.__dimensions:
            # print('{} items left'.format(sum(1 if e is None else 0 for e in self.__errors)))
            self.end_error = error
            if None not in self.__errors:
                self.__sort_parameters()
                getattr(self, 'calculate_' + self.__step())()
        elif self.__step == 'shrink':
            # print('{} items left'.format(sum(1 if e is None else 0 for e in self.__errors)))
            self.__errors[index] = error
            if None not in self.__errors and self.end_error is not None:
                self.__sort_parameters()
                getattr(self, 'calculate_' + getattr(self, self.__step)())()

        elif self.__step == 'start' and index == self.__dimensions:
            self.end_error = error
            if None not in self.__errors:
                # print('Started reflection')
                self.__sort_parameters()
                self.calculate_reflection()
            else:
                # print('{} items left'.format(sum(1 if e is None else 0 for e in self.__errors)))
        elif self.__step == 'start':
            self.__errors[index] = error
            if None not in self.__errors and self.end_error is not None:
                # print('Started reflection')
                self.__sort_parameters()
                self.calculate_reflection()
            elif None in self.__errors:
                # print('{} items left'.format(sum(1 if e is None else 0 for e in self.__errors)))
            else:
                # print('One item left')

    def __sort_parameters(self):
        indices = argsort(self.__errors + [self.end_error])
        parameters = []
        errors = []

        for i in indices[:-1]:
            if i == self.__dimensions:
                parameters.append(self.__end)
                errors.append(self.end_error)
            else:
                parameters.append(self.__parameters[i])
                errors.append(self.__errors[i])

        if indices[-1] != self.__dimensions:
            self.end_error = self.__errors[indices[-1]]
            self.__end = self.__parameters[indices[-1]]

        self.__parameters = parameters
        self.__errors = errors
        # # print(self.__errors)

    def calculate_centroid(self):
        self.__centroid = mean(self.__parameters, axis=0)

    def calculate_reflection(self):
        self.__step = 'reflection'
        self.calculate_centroid()
        self.__reflection = self.__centroid + self.__alpha * \
            (self.__centroid - self.__end)
        self.__request_normals(self.__reflection)

    def reflection(self):
        self.__sort_parameters()
        if self.reflection_error < self.__errors[0]:
            return 'expansion'
        elif self.reflection_error >= self.__errors[-1]:
            return 'contraction'
        else:
            # print('R, E1, En:', self.reflection_error, self.__errors[0], self.__errors[-1])
            self.__end = self.__reflection
            self.end_error = self.reflection_error
            return 'reflection'

    def calculate_expansion(self):
        self.__step = 'expansion'
        self.__expansion = self.__centroid + self.__gamma * \
            (self.__reflection - self.__centroid)
        self.__request_normals(self.__expansion)

    def expansion(self):
        if self.expansion_error < self.reflection_error:
            self.__end = self.__expansion
            self.end_error = self.expansion_error
        else:
            self.__end = self.__reflection
            self.end_error = self.reflection_error
        return 'reflection'

    def calculate_contraction(self):
        self.__step = 'contraction'
        self.__contraction = self.__centroid + self.__rho * \
            (self.__parameters[-1] - self.__centroid)
        self.__request_normals(self.__contraction)

    def contraction(self):
        if self.contraction_error < self.end_error:
            self.__end = self.__contraction
            self.end_error = self.contraction_error
            return 'reflection'
        return 'shrink'

    def calculate_shrink(self):
        self.__step = 'shrink'
        self.__parameters[1:] = self.__parameters[0] + self.__sigma * \
            (self.__parameters[1:] - self.__parameters[0])
        self.__errors[1:] = [None] * (len(self.__errors) - 1)

        self.__end = self.__parameters[0] + self.__sigma * \
            (self.__end - self.__parameters[0])
        self.end_error = None

        for i in range(1, self.__dimensions):
            self.__request_normals(self.__parameters[i], i)
        self.__request_normals(self.__end, self.__dimensions)

    def shrink(self):
        if self.__finished():
            return 'finish'
        else:
            return 'reflection'

    def calculate_finish(self):
        self.__step = 'finish'
        # print(self.__parameters[0])
        # print(self.__errors[0])
        # print(self.__light)

        img = self.__normals.dot(self.__light)[::-1]
        alpha = zeros(len(self.__normals[:, 3]))
        alpha[nonzero(self.__normals[:, 3])[0]] = 1.
        # print('Results', img, nonzero(self.__normals[:, 3])[0])
        data = (column_stack((
                img, img, img,
                alpha
                )) * 255).astype('i')
        # pixels = [(data[i*4+0], data[i*4+1], data[i*4+2], data[i*4+3])
        #            for i in range(500*500-1, -1, -1)]
        # pixels = list(zip(data))
        image = Image.new('L', (500, 500))
        image.putdata((img*255).astype('i'))
        image.save('img.png')

    def __finished(self):
        s = 0.
        for i in range(1, len(self.__parameters)):
            s += norm(self.__parameters[i] - self.__parameters[i-1])
        # print('Perimeter is', s)
        return s < 50.
