"""Utilities for work with shaders files."""
from os.path import dirname, abspath, join

SHADERS_FOLDER = dirname(abspath(__file__))


def get_shader_path(filename):
    """Get full path to shader file."""
    return join(SHADERS_FOLDER, filename)
