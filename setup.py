from distutils.core import setup, Extension
from os.path import join
import numpy.distutils.misc_util

SOURCES_DIR = 'libs'
C_EXTENSION = '.c'
WRAPPER_PREFIX = '_'

def get_sources(name):
    filename = name + C_EXTENSION
    return [join(SOURCES_DIR, n) for n in [filename, WRAPPER_PREFIX + filename]]

normals = Extension('src.normals', get_sources('normals'))
face = Extension('src.face', get_sources('face'))

setup(ext_modules=[normals, face],
      include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs())
