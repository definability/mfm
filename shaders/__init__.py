from os.path import dirname, abspath, join

SHADERS_FOLDER = dirname(abspath(__file__))


def get_shader_path(filename):
    return join(SHADERS_FOLDER, filename)
