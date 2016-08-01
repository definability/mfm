import sys

from OpenGL.GL import GL_LESS, GL_TRUE, GL_DEPTH_TEST, GL_STENCIL_TEST
from OpenGL.GL import GL_COLOR_ARRAY, GL_VERTEX_ARRAY, GL_TRIANGLES
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GL import GL_UNSIGNED_SHORT, GL_FLOAT, GL_MODELVIEW
from OpenGL.GL import GL_CULL_FACE, GL_FRONT, GL_MODELVIEW_MATRIX

from OpenGL.GL import glMatrixMode, glLoadIdentity, glOrtho, glRotatef
from OpenGL.GL import glDepthMask, glDepthFunc, glCullFace
from OpenGL.GL import glEnable, glClearColor, glEnableClientState, glClear
from OpenGL.GL import glDrawElements, glGetFloatv

from OpenGL.GL import glReadBuffer, glReadPixels, GL_BACK, GL_RGBA

from OpenGL.GLUT import GLUT_DOUBLE, GLUT_DEPTH, GLUT_RGB

from OpenGL.GLUT import glutInitWindowSize, glutSwapBuffers, glutPostRedisplay
from OpenGL.GLUT import glutCreateWindow, glutInit, glutInitWindowPosition
from OpenGL.GLUT import glutInitDisplayMode, glutLeaveMainLoop, glutDisplayFunc

from numpy import zeros, array

from shaders import ShadersHelper


class View:
    """Viewport for Faces."""

    __triangles = None
    __triangles_size = None

    def __init__(self, size):
        """Initialize viewport with initial Face rotation and position."""
        self.__size = size

        self.__vertices = None
        self.__colors = None
        self.__normals = None
        self.__rotation = (0., 0., 0.)
        self.__position = (0., 0., 0.)

        self.__init_display()
        self.__adjust_viewport()
        self.__enable_depth_test()

        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)

        glClearColor(1., 1., 1., 0.)

        self.__sh = ShadersHelper('face.vert', 'face.frag', 2)

        glutDisplayFunc(self.__display)
        self.__callback = None

    def get_size(self):
        """Get size of the viewport."""
        return self.__size

    def update(self, vertices=None, colors=None, rotation=None, position=None):
        """Change model parameters.

        Allows to replace vertices, colors, rotation and position
        of displayed model.

        When you replace the vertices, it means that you change shape.
        """
        self.__vertices = vertices if vertices is not None else self.__vertices
        self.__colors = colors if colors is not None else self.__colors
        self.__rotation = rotation if rotation is not None else self.__rotation
        self.__position = position if position is not None else self.__position

    def redraw(self, callback=None):
        """Trigger redisplay and trigger callback after render."""
        # print('Set callback to', callback)
        self.__callback = callback
        glutPostRedisplay()

    def get_image(self):
        """Copy RGBA data from the viewport to NumPy Matrix of float."""
        glReadBuffer(GL_BACK)
        height, width = self.__size
        data = zeros(width*height*4, dtype='f')
        glReadPixels(0, 0, width, height, GL_RGBA, GL_FLOAT, data)
        return data

    def close(self):
        """Close the viewport."""
        glutLeaveMainLoop()

    @staticmethod
    def set_triangles(triangles, triangles_size):
        """Set triangles of the model.

        Accepts C array of ints, which contains triangles
        as indices of vertices.
        Allows to not allocate additional memory for each point,
        which is used in multiple triangles.
        """
        View.__triangles = triangles
        View.__triangles_size = triangles_size

    def __display(self):
        """Render the model by existent vertices, colors and triangles."""
        glRotatef(1., *self.__rotation)
        rotation_matrix = array(glGetFloatv(GL_MODELVIEW_MATRIX), dtype='f')

        self.__sh.add_attribute(0, self.__vertices, 'vin_position')
        self.__sh.add_attribute(1, self.__colors, 'vin_color')
        self.__sh.bind_buffer()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.__sh.use_shaders()

        self.__sh.bind_uniform_matrix(rotation_matrix, 'rotation_matrix')

        glDrawElements(GL_TRIANGLES, View.__triangles_size,
                       GL_UNSIGNED_SHORT, View.__triangles)

        self.__sh.clear()

        glutSwapBuffers()
        if self.__callback is not None:
            self.__callback()

    def __init_display(self):
        """Initialize the viewport with specified size."""
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
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
                -SIDE_LENGTH, SIDE_LENGTH)

    def __enable_depth_test(self):
        """Enable depth test and faces culling.

        Needed to not render invisible vertices and triangles.
        """
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
