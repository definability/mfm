from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from numpy import array, column_stack, zeros
from numpy.random import randn

from load_model import morph
from src import Face


def render_face(model):
    init(model)

    rotations = {
        'x': 0.,
        'y': 0.,
        'z': 0.
    }
    glutDisplayFunc(lambda: draw(model, rotations))

    glutKeyboardFunc(lambda key, x, y:
                     keyboard(rotations, key, x, y, False, False, model))
    glutKeyboardUpFunc(lambda key, x, y:
                     keyboard(rotations, key, x, y, True, False, model))
    glutSpecialFunc(lambda key, x, y:
                    keyboard(rotations, key, x, y, False, True, model))
    glutSpecialUpFunc(lambda key, x, y:
                      keyboard(rotations, key, x, y, True, True, model))

    glutMainLoop()


def init(model):
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(300, 300)

    glutInitWindowPosition(50, 50)
    glutInit(sys.argv)
    glutCreateWindow(b"Morphable face model")

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    side = .5
    glOrtho(-side, side, -side, side, -side, side)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glClearColor(1., 1., 1., 0.)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)

    calculate(model)


def draw(model, rotations):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1., rotations['x'], rotations['y'], rotations['z'])
    glVertexPointer(3, GL_FLOAT, 0, model['face'].get_vertices_c())
    colors = model['face'].get_light_map_c() if model['light'] \
             else model['face'].get_normal_map_c()
    glColorPointer(3, GL_FLOAT, 0, colors);
    glDrawElements(GL_TRIANGLES, model['face'].get_triangles().size,
                   GL_UNSIGNED_SHORT, model['face'].get_triangles_c())
    glutSwapBuffers()

    #glReadBuffer(GL_BACK)
    #height, width = 300, 300
    #data = zeros(width*height*4, dtype='f')
    #glReadPixels(0, 0, width, height, GL_RGBA, GL_FLOAT, data)


def keyboard(rotations, key, x, y, release=False, special=True, model=None):
    directions = {}
    if special:
        directions = {
            GLUT_KEY_UP: ('x', -1.),
            GLUT_KEY_DOWN: ('x', 1.),
            GLUT_KEY_RIGHT: ('y', -1.),
            GLUT_KEY_LEFT: ('y', 1.)
        }
    else:
        directions = {
            b'z': ('z', -1.),
            b'a': ('z', 1.)
        }
        if key == b'q':
            return glutLeaveMainLoop()
        if key == b'n' and not release:
            model['light'] = not model['light']
        if key == b'r' and not release:
            calculate(model)
    if key in directions:
        axis, value = directions[key]
        rotations[axis] = 0. if release else value
    glutPostRedisplay()


def calculate(model, redraw=True):
    if redraw:
        coordinates = morph(model['mfm'], randn(199, 1)).astype('f')
        #coordinates = morph(model, zeros(199).reshape(199, 1)).astype('f')
        #coordinates = model['shapeMU']

        model['face'] = Face(coordinates, [-1, 0, -1])

