import sys

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
from OpenGL.GL import GL_TEXTURE0, GL_FRAMEBUFFER

from OpenGL.GL import glReadBuffer, glReadPixels, GL_RGBA, glPolygonOffset
from OpenGL.GL import GL_POLYGON_OFFSET_FILL

from OpenGL.GLUT import GLUT_DEPTH, GLUT_RGB, GLUT_ALPHA, GLUT_DOUBLE

from OpenGL.GLUT import glutSwapBuffers, glutMainLoop
from OpenGL.GLUT import glutInitWindowSize, glutPostRedisplay
from OpenGL.GLUT import glutCreateWindow, glutInit, glutInitWindowPosition
from OpenGL.GLUT import glutInitDisplayMode, glutLeaveMainLoop, glutDisplayFunc

from OpenGL.GLU import gluLookAt

from numpy import zeros, array

from .ShadersHelper import ShadersHelper
from .normals import get_normals
from .face import calculate_face, init_face_calculator


class View:
    """Viewport for Faces."""

    __triangles = None
    __principal_components = None
    __principal_components_flattened = None
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
        self.__face_vertices = None
        self.__model_matrix = zeros((4, 4), dtype='f')
        self.__light_matrix = zeros((4, 4), dtype='f')

        self.__init_display()
        self.__enable_depth_test()

        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        glClearColor(1., 1., 1., 0.)

        self.__sh = ShadersHelper(['face.vert', 'depth.vert'],
                                  ['face.frag', 'depth.frag'], 2, 1)

        glutDisplayFunc(self.__display)
        self.__callback = None

        self.__sh.add_attribute(0, array([]), 'face_vertices')
        self.__sh.add_attribute(1, array([]), 'normal_vector')
        self.__sh.bind_buffer()
        self.__sh.use_shaders()
        self.__sh.link_texture('depth_map', 0)
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

        self.__face_vertices = calculate_face(self.__face.coefficients)

        vertices_count = self.__face_vertices.size // 3
        vertices = self.__face_vertices.reshape(vertices_count, 3)
        vertices -= (vertices.max(axis=0) + vertices.min(axis=0)) / 2

        scales = vertices.max(axis=0) - vertices.min(axis=0)
        vertices /= scales * self.__face.scale

        self.__face_vertices = vertices.reshape(self.__face_vertices.size, 1)

    def redraw(self, callback=None):
        """Trigger redisplay and trigger callback after render."""
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
        View.__principal_components_flattened = principal_components.flatten()

    @staticmethod
    def set_deviations(deviations):
        """Get principal components deviations."""
        View.__deviations = deviations

    @staticmethod
    def set_mean_face(mean_face):
        """Set mean Face for modelling."""
        View.__mean_face = mean_face

    @staticmethod
    def finalize_initialization():
        """Initialize C methods."""
        init_face_calculator(
            View.__mean_face,
            View.__principal_components_flattened,
            View.__deviations)

    @staticmethod
    def __get_rotation_matrix(coordinates, side_length):
        """Get rotation matrix from specific point of view and scale."""
        assert len(coordinates) == 3
        glLoadIdentity()
        glOrtho(-side_length, side_length, -side_length, side_length,
                -4 * side_length, 4 * side_length)
        x, y, z = coordinates
        gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
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

        light = self.__face.directed_light_cartesian
        self.__light_matrix = self.__get_rotation_matrix(
            (light[0], light[1], light[2]), 1.0)

    def __generate_shadows(self):
        """Generate shadow matrix for rotated model."""
        glDisable(GL_CULL_FACE)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(3, 0)

        self.__sh.change_shader(vertex=1, fragment=1)
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

        self.__sh.change_shader(vertex=0, fragment=0)
        self.__prepare_shaders(self.__model_matrix, self.__light_matrix, False)
        self.__sh.bind_buffer()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, View.__triangles.size,
                       GL_UNSIGNED_SHORT, View.__triangles)
        self.__sh.clear()

    def __prepare_shaders(self, rotation_matrix=None, light_matrix=None,
                          depth=True):
        """Generic shaders preparation method for depth map and final scene."""
        self.__sh.add_attribute(0, self.__face_vertices, 'face_vertices')
        self.__sh.bind_buffer()

        self.__sh.use_shaders()

        self.__sh.bind_uniform_matrix(light_matrix, 'light_matrix')
        if not depth:
            face = self.__face_vertices.reshape(self.__mean_face.size // 3, 3)
            normals = get_normals(face, View.__triangles.flatten())
            self.__sh.add_attribute(1, normals, 'normal_vector')

            self.__sh.bind_uniform_matrix(rotation_matrix, 'rotation_matrix')
            self.__sh.bind_uniform_vector(self.__face.light_cartesian,
                                          'light_vector')

        if not depth:
            glActiveTexture(GL_TEXTURE0)
            self.__sh.bind_texture(0)

    def __init_display(self):
        """Initialize the viewport with specified size."""
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(*self.__size)

        glutInitWindowPosition(0, 0)
        glutInit(sys.argv)
        glutCreateWindow(b"Morphable face model")

    def start(self):
        """Run main loop.

        Blocking operation.
        Should be executed after all initial actions.
        """
        glutMainLoop()

    def __enable_depth_test(self):
        """Enable depth test and faces culling.

        Needed to not render invisible vertices and triangles.
        """
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        glCullFace(GL_FRONT)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
