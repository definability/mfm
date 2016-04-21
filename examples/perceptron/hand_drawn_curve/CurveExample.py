from random import random
from numpy import linspace

class CurveExample:
    def __init__(self, perceptron, A,
            inside_points, outside_points,
            order, x_limits, y_limits, resolution):
        self.perceptron = perceptron
        self.A = A
        self.inside_points = inside_points
        self.outside_points = outside_points
        self.order = order

        self.x_limits = x_limits
        self.x_range = self.x_limits[1] - self.x_limits[0]
        self.y_limits = y_limits
        self.y_range = self.y_limits[1] - self.y_limits[0]

        self.resolution = resolution
        self.cache = {}
        self.grid = self.generate_grid(self.x_limits, self.y_limits,
                                       self.resolution)


    def generate_grid(self, x_limits, y_limits, resolution):
        return (linspace(x_limits[0], x_limits[1], resolution),
                linspace(y_limits[0], y_limits[1], resolution))


    def generate_point(self):
        new_x = random() * self.x_range + self.x_limits[0]
        new_y = random() * self.y_range + self.y_limits[0]
        return (new_x, new_y)

