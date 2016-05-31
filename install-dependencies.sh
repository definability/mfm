#!/bin/bash

apt update
apt install -y python-opengl python-numpy python-scipy

pip install --upgrade pip
pip install scipy numpy pyopengl ipython pillow
pip install pylint pep8

