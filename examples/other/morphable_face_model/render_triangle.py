from numpy import array, column_stack, zeros
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *


def rasterize_triangles(vertices, triangles, colors):
    vertices = vertices - vertices.min()
    vertices /= vertices.max()
    return render_face(vertices, colors, triangles)


def render_face(vertices, colors, triangles):
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(300, 300)

    glutInitWindowPosition(50, 50)
    glutInit(sys.argv)
    glutCreateWindow(b"Happy New Year!")

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.5, 1.5)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glClearColor(1., 1., 1., 0.)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)

    rotations = {
        'x': 0.,
        'y': 0.,
        'z': 0.
    }
    glutDisplayFunc(lambda: draw(vertices, colors, triangles, rotations))

    glutKeyboardFunc(lambda key, x, y:
                     keyboard(rotations, key, x, y, False, False))
    glutKeyboardUpFunc(lambda key, x, y:
                     keyboard(rotations, key, x, y, True, False))
    glutSpecialFunc(lambda key, x, y:
                    keyboard(rotations, key, x, y, False, True))
    glutSpecialUpFunc(lambda key, x, y:
                      keyboard(rotations, key, x, y, True, True))

    glutMainLoop()


def draw(vertices, colors, triangles, rotations):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1., rotations['x'], rotations['y'], rotations['z'])
    glVertexPointer(3, GL_FLOAT, 0, vertices.ctypes.get_as_parameter())
    glColorPointer(3, GL_FLOAT, 0, colors.ctypes.get_as_parameter());
    glDrawElements(GL_TRIANGLES, triangles.size, GL_UNSIGNED_SHORT,
                   triangles.ctypes.get_as_parameter())
    glutSwapBuffers()

    #glReadBuffer(GL_BACK)
    #height, width = 300, 300
    #data = zeros(width*height*4, dtype='uint8')
    #glReadPixels(0,0,width,height, GL_RGBA, GL_UNSIGNED_BYTE, data)


def keyboard(rotations, key, x, y, release=False, special=True):
    directions = {}
    if special:
        directions = {
            GLUT_KEY_UP: ('x', -1.),
            GLUT_KEY_DOWN: ('x', 1.),
            GLUT_KEY_LEFT: ('y', -1.),
            GLUT_KEY_RIGHT: ('y', 1.),
        }
    else:
        directions = {
            b'z': ('z', -1.),
            b'a': ('z', 1.)
        }
    if not special and key == b'q':
        glutLeaveMainLoop()
    if key in directions:
        axis, value = directions[key]
        rotations[axis] = 0. if release else value
    glutPostRedisplay()

