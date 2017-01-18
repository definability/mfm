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
    version='0.8.3',
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
             ['data', 'shaders'],
    install_requires=[
        'argparse',
        'cairocffi==0.7.2',
        'Pillow==3.2.0',
        'PyOpenGL==3.1.0',
    ],
    extras_require={
        'dev': [
            'flake8==2.6.2',
            'pylint==1.5.5',
        ]
    },
    setup_requires=[
        'pytest-runner==2.9'
    ],
    tests_require=[
        'pytest==3.0.5',
        'pytest-cov==2.4.0',
        'coveralls==1.1',
    ]
)
