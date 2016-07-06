from unittest import TestCase
from numpy import array, allclose, load
from PIL import Image

from src.fitter import ModelFitter
from data import get_datafile_path


class ModelFitterTest(TestCase):
    def test_constructor(self):
        self.assertIsInstance(ModelFitter(array([])), ModelFitter)

    def test_estimate_light(self):
        N = array([[1, 0, 1, 1],
                   [0, 1, 1, 1],
                   [1, 2, 2, 1]])
        light = array([.5, .1, 1., 0.])
        image = N.dot(light)

        fit = ModelFitter(image)
        x = fit.estimate_light(N)
        self.assertTrue(allclose(N.dot(x), N.dot(light)))

    def test_estimate_light_face(self):
        normals_filename = get_datafile_path('test.npy')
        model_filename = get_datafile_path('test.png')
        light_filename = get_datafile_path('test.light.npy')

        real_light = load(light_filename)
        normals = load(normals_filename)

        image = Image.open(model_filename).convert('L')
        shadows = array(image.getdata()).astype('f') / 255
        image.close()

        fit = ModelFitter(shadows)
        x = fit.estimate_light(normals)

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
