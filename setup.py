from setuptools import Extension, setup, find_packages
from os.path import join, dirname
import numpy.distutils.misc_util

SOURCES_DIR = 'libs'
C_EXTENSION = '.c'
WRAPPER_PREFIX = '_'

def get_sources(name):
    filename = name + C_EXTENSION
    return [join(SOURCES_DIR, n) for n in [filename, WRAPPER_PREFIX + filename]]

normals = Extension('src.normals', get_sources('normals'))
face = Extension('src.face', get_sources('face'))

long_description=''
with open(join(dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    ext_modules=[normals, face],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
    name='MFM',
    version='0.3.2',
    license='MIT',
    description='Morphable Face Model fitting application',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=[join('src', p) for p in find_packages('src')] + \
             [join('tests', p) for p in find_packages('tests')] + \
             ['data', 'shaders'],
    install_requires=[
        'argparse==1.1.0',
        'cairocffi==0.7.2',
        'enum34==1.1.6',
        'Pillow==3.2.0',
        'PyOpenGL==3.1.0',
    ],
    extras_require={
        'dev': [
            'flake8==2.6.2',
            'pylint==1.5.5'
        ]
    },
    test_suite='tests'
)
