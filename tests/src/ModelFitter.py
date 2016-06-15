from unittest import TestCase
from numpy import array, allclose, load
from PIL import Image

from src import ModelFitter
from data import get_datafile_path


class ModelFitterTest(TestCase):
    def test_constructor(self):
        self.assertIsInstance(ModelFitter(array([])), ModelFitter)

    def test_check(self):
        N = array([[1, 0, 1, 1],
                   [0, 1, 1, 1],
                   [1, 2, 2, 1]])
        light = array([.5, .1, 1., 0.])
        image = N.dot(light)

        fit = ModelFitter(image)
        x = fit.check(N)
        self.assertTrue(allclose(N.dot(x), N.dot(light)))

    def test_check_face(self):
        real_light = [0.337397462814, -0.496287279542,
                     -0.560942790202, -0.050649723592442575]
        normals_filename = get_datafile_path('test.npy')
        model_filename = get_datafile_path('test.png')

        normals = load(normals_filename)

        image = Image.open(model_filename).convert('L')
        shadows = array(image.getdata()).astype('f') / 255
        image.close()

        fit = ModelFitter(shadows)
        x = fit.check(normals)

        result = get_image(normals, x)
        real_result = get_image(normals, real_light)

        data = get_difference(result, shadows, normals)
        real_data = get_difference(real_result, shadows, normals)

        self.assertLessEqual(data.sum(), real_data.sum())

def get_image(normals, light):
    result = normals.dot(light)
    # TODO: results should be cut to these borders
    # result[result < 0.] = 0.
    # result[result > 1.] = 1.
    return result

def get_difference(result, shadows, normals):
    difference = (result - shadows)**2
    difference[normals[:, 3] == 0.] = 0.
    return difference
