from numpy import array, column_stack
import ctypes

render_face = ctypes.cdll.LoadLibrary('./lib_render_face.so')

def rasterize_triangles(vertices, triangles, colors):
    vertices = vertices - vertices.min()
    vertices /= vertices.max()
    return render_face.render_face(vertices.ctypes.get_as_parameter(),
                                   colors.ctypes.get_as_parameter(),
                                   triangles.ctypes.get_as_parameter(),
                                   triangles.size)

