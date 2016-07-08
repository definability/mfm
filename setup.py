from distutils.core import setup, Extension
import numpy.distutils.misc_util

normals = Extension("src.normals", ["libs/_normals.c", "libs/normals.c"])

setup(ext_modules=[normals],
      include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs())
