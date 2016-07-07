from distutils.core import setup, Extension
import numpy.distutils.misc_util

setup(
    ext_modules=[Extension("src.cross", ["libs/_cross.c", "libs/cross.c"])],
    include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs()
)
