import sys
from math import ceil

from OpenGL.GL import GL_LESS, GL_TRUE, GL_DEPTH_TEST, GL_STENCIL_TEST
from OpenGL.GL import GL_COLOR_ARRAY, GL_VERTEX_ARRAY, GL_TRIANGLES
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GL import GL_UNSIGNED_SHORT, GL_FLOAT, GL_MODELVIEW
from OpenGL.GL import GL_CULL_FACE, GL_FRONT, GL_MODELVIEW_MATRIX

from OpenGL.GL import glMatrixMode, glLoadIdentity, glOrtho, glRotatef
from OpenGL.GL import glDepthMask, glDepthFunc, glCullFace, glDisable
from OpenGL.GL import glEnable, glClearColor, glEnableClientState, glClear
from OpenGL.GL import glDrawElements, glGetFloatv, glLoadMatrixf, glFinish
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
        self.__rotation = (0., 0., 0.)
        self.__need_rotation = True
        self.__face = None
        self.__light_matrix = zeros((4, 4), dtype='f')

        self.__init_display()
        self.__adjust_viewport()
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
        self.__bind_texture()
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
    def rotation(self):
        """Get model rotation."""
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation):
        """Set model rotation."""
        self.__need_rotation = True
        self.__rotation = rotation

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

    def __display(self):
        """Render the model by existent vertices, colors and triangles."""
        if self.__need_rotation:
            glRotatef(1., *self.__rotation)
            self.__need_rotation = False
        rotation_matrix = array(glGetFloatv(GL_MODELVIEW_MATRIX), dtype='f')

        # GET SHADOWS
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(3, 0)
        self.__sh.change_shader(vertex=1, fragment=1)

        glLoadMatrixf(self.__light_matrix.flatten())
        glLoadIdentity()
        SIDE_LENGTH = 2.0
        glOrtho(-SIDE_LENGTH, SIDE_LENGTH, -SIDE_LENGTH, SIDE_LENGTH,
                -2 * SIDE_LENGTH, 2 * SIDE_LENGTH)
        light = self.__face.directed_light
        gluLookAt(-light[0], -light[1], light[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        self.__light_matrix = array(glGetFloatv(GL_MODELVIEW_MATRIX), dtype='f')
        glLoadMatrixf(rotation_matrix.flatten())

        glDisable(GL_CULL_FACE)
        self.__prepare_shaders(rotation_matrix, self.__light_matrix, True)
        self.__sh.bind_fbo()
        glClear(GL_DEPTH_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, View.__triangles.size,
                       GL_UNSIGNED_SHORT, View.__triangles)
        glFinish()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.__sh.clear()

        # RENDER
        # glViewport(0, 0, self.__width, self.__height)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.__sh.change_shader(vertex=0, fragment=0)
        self.__prepare_shaders(rotation_matrix, self.__light_matrix, False)
        self.__sh.bind_buffer()
        self.__sh.use_shaders()
        glDrawElements(GL_TRIANGLES, View.__triangles.size,
                       GL_UNSIGNED_SHORT, View.__triangles)
        self.__sh.clear()

        glutSwapBuffers()
        if self.__callback is not None:
            self.__callback()

    def __prepare_shaders(self, rotation_matrix=None, light_matrix=None,
                          depth=True):
        """Generic shaders preparation method for depth map and final scene."""
        self.__sh.add_attribute(0, self.__mean_face, 'mean_position')
        self.__sh.bind_buffer()

        self.__sh.use_shaders()

        self.__sh.bind_uniform_matrix(light_matrix.dot(rotation_matrix), 'light_matrix')
        if not depth:
            self.__sh.bind_uniform_matrix(rotation_matrix, 'rotation_matrix')
            self.__sh.bind_uniform_vector(self.__face.light,
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

    def __bind_texture(self):
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

    def __adjust_viewport(self):
        """Initialize rotation matrix and viwport box."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        SIDE_LENGTH = .5
        glOrtho(-SIDE_LENGTH, SIDE_LENGTH, -SIDE_LENGTH, SIDE_LENGTH,
                -2 * SIDE_LENGTH, 2 * SIDE_LENGTH)

    def __enable_depth_test(self):
        """Enable depth test and faces culling.

        Needed to not render invisible vertices and triangles.
        """
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
