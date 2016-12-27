import sys
from math import ceil

from OpenGL.GL import GL_LESS, GL_TRUE, GL_DEPTH_TEST, GL_STENCIL_TEST
from OpenGL.GL import GL_COLOR_ARRAY, GL_VERTEX_ARRAY, GL_TRIANGLES
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GL import GL_UNSIGNED_SHORT, GL_FLOAT
from OpenGL.GL import GL_CULL_FACE, GL_FRONT, GL_MODELVIEW_MATRIX

from OpenGL.GL import glLoadIdentity, glOrtho
from OpenGL.GL import glDepthMask, glDepthFunc, glCullFace, glDisable
from OpenGL.GL import glEnable, glClearColor, glEnableClientState, glClear
from OpenGL.GL import glDrawElements, glGetFloatv, glFinish
from OpenGL.GL import glActiveTexture, glBindFramebuffer
from OpenGL.GL import GL_TEXTURE0, GL_TEXTURE1, GL_FRAMEBUFFER

from OpenGL.GL import glReadBuffer, glReadPixels, GL_RGBA, glPolygonOffset
from OpenGL.GL import GL_POLYGON_OFFSET_FILL

from OpenGL.GLUT import GLUT_DEPTH, GLUT_RGB, GLUT_ALPHA, GLUT_DOUBLE

from OpenGL.GLUT import glutSwapBuffers
from OpenGL.GLUT import glutInitWindowSize, glutPostRedisplay
from OpenGL.GLUT import glutCreateWindow, glutInit, glutInitWindowPosition
from OpenGL.GLUT import glutInitDisplayMode, glutLeaveMainLoop, glutDisplayFunc

from OpenGL.GLU import gluLookAt

from numpy import zeros, ones, array, concatenate

from .ShadersHelper import ShadersHelper


class View:
    """Viewport for Faces."""

    __triangles = None
    __principal_components = None
    __deviations = None
    __mean_face = None

    def __init__(self, size):
        """Initialize viewport with initial Face rotation and position."""
        self.__size = size

        self.__height, self.__width = self.__size
        self.__output_image = zeros(self.__width * self.__height * 4,
                                    dtype='f')

        self.__light = None
        self.__face = None
        self.__model_matrix = zeros((4, 4), dtype='f')
        self.__light_matrix = zeros((4, 4), dtype='f')

        self.__init_display()
        self.__enable_depth_test()

        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        glClearColor(1., 1., 1., 0.)

        self.__sh = ShadersHelper(['face.vert', 'depth.vert'],
                                  ['face.frag', 'depth.frag'], 1, 2)

        glutDisplayFunc(self.__display)
        self.__callback = None

        self.__sh.add_attribute(0, self.__mean_face, 'mean_position')
        self.__sh.bind_buffer()
        self.__sh.use_shaders()
        self.__sh.link_texture('principal_components', 0)
        self.__sh.link_texture('depth_map', 1)
        self.__bind_pca_texture()
        self.__sh.bind_depth_texture(self.__size)

    def get_size(self):
        """Get size of the viewport."""
        return self.__size

    @property
    def light(self):
        """Get light direction."""
        return self.__light

    @light.setter
    def light(self, light):
        """Set light direction."""
        self.__light = light

    @property
    def face(self):
        """Get current Face."""
        return self.__face

    @face.setter
    def face(self, face):
        """Set current Face."""
        self.__face = face

    def redraw(self, callback=None):
        """Trigger redisplay and trigger callback after render."""
        # print('Set callback to', callback)
        self.__callback = callback
        glutPostRedisplay()

    def get_image(self):
        """Copy RGBA data from the viewport to NumPy Matrix of float."""
        glReadBuffer(GL_FRONT)
        glReadPixels(0, 0, self.__width, self.__height, GL_RGBA, GL_FLOAT,
                     self.__output_image)
        return self.__output_image

    def close(self):
        """Close the viewport."""
        glutLeaveMainLoop()

    @staticmethod
    def set_triangles(triangles):
        """Set triangles of the model.

        Allows to not allocate additional memory for each point,
        which is used in multiple triangles.
        """
        View.__triangles = triangles

    @staticmethod
    def set_principal_components(principal_components):
        """Set principal components for Face calculation."""
        View.__principal_components = principal_components

    @staticmethod
    def set_deviations(deviations):
        """Get principal components deviations."""
        View.__deviations = deviations

    @staticmethod
    def set_mean_face(mean_face):
        """Set mean Face for modelling."""
        View.__mean_face = mean_face

    @staticmethod
    def __get_rotation_matrix(coordinates, side_length):
        """Get rotation matrix from specific point of view and scale."""
        assert len(coordinates) == 3
        glLoadIdentity()
        glOrtho(-side_length, side_length, -side_length, side_length,
                -4 * side_length, 4 * side_length)
        x, y, z = coordinates
        gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        return array(glGetFloatv(GL_MODELVIEW_MATRIX), dtype='f')

    def __display(self):
        """Render the model by existent vertices, colors and triangles."""
        self.__rotate_model()
        self.__generate_shadows()
        self.__generate_model()

        glutSwapBuffers()
        if self.__callback is not None:
            self.__callback()

    def __rotate_model(self):
        """Update model rotation matrix."""
        self.__model_matrix = self.__get_rotation_matrix(
            self.__face.position_cartesian,
            (1 + self.__face.position[2]) * 0.5)

    def __generate_shadows(self):
        """Generate shadow matrix for rotated model."""
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(3, 0)
        self.__sh.change_shader(vertex=1, fragment=1)

        light = self.__face.directed_light_cartesian
        self.__light_matrix = self.__get_rotation_matrix(
            (light[0], light[1], -light[2]), 2.0)

        glDisable(GL_CULL_FACE)
        self.__prepare_shaders(self.__model_matrix, self.__light_matrix, True)
        self.__sh.bind_fbo()
        glClear(GL_DEPTH_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, View.__triangles.size,
                       GL_UNSIGNED_SHORT, View.__triangles)
        glFinish()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.__sh.clear()

    def __generate_model(self):
        """Generate rotated model with shadows."""
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.__sh.change_shader(vertex=0, fragment=0)
        self.__prepare_shaders(self.__model_matrix, self.__light_matrix, False)
        self.__sh.bind_buffer()
        self.__sh.use_shaders()
        glDrawElements(GL_TRIANGLES, View.__triangles.size,
                       GL_UNSIGNED_SHORT, View.__triangles)
        self.__sh.clear()

    def __prepare_shaders(self, rotation_matrix=None, light_matrix=None,
                          depth=True):
        """Generic shaders preparation method for depth map and final scene."""
        self.__sh.add_attribute(0, self.__mean_face, 'mean_position')
        self.__sh.bind_buffer()

        self.__sh.use_shaders()

        self.__sh.bind_uniform_matrix(light_matrix.dot(rotation_matrix),
                                      'light_matrix')
        if not depth:
            self.__sh.bind_uniform_matrix(rotation_matrix, 'rotation_matrix')
            self.__sh.bind_uniform_vector(self.__face.light_cartesian,
                                          'light_vector')
        coefficients_amount = len(self.__face.coefficients)
        indices = -ones(199, dtype='i')
        indices[:coefficients_amount] = array(range(coefficients_amount))
        self.__sh.bind_uniform_ints(indices, 'indices')

        coefficients = zeros(199, dtype='f')
        coefficients[:coefficients_amount] = self.__face.coefficients
        self.__sh.bind_uniform_floats(coefficients, 'coefficients')

        glActiveTexture(GL_TEXTURE0)
        self.__sh.bind_texture(0)
        if not depth:
            glActiveTexture(GL_TEXTURE1)
            self.__sh.bind_texture(1)

    def __bind_pca_texture(self):
        """Bind texture with principal components.

        Needed for shaders to calculate Face model.
        """
        size = View.__principal_components.size // 3
        data = View.__principal_components.transpose() * View.__deviations

        columns = 2**13
        rows = ceil(size / columns)

        padding = [0] * (rows * columns - size) * 3
        data = concatenate((data.flatten(), padding))

        self.__sh.create_float_texture(data, (columns, rows), 2, 3)

    def __init_display(self):
        """Initialize the viewport with specified size."""
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(*self.__size)

        glutInitWindowPosition(0, 0)
        glutInit(sys.argv)
        glutCreateWindow(b"Morphable face model")

    def __enable_depth_test(self):
        """Enable depth test and faces culling.

        Needed to not render invisible vertices and triangles.
        """
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
