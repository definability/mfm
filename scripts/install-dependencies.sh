#!/bin/bash

apt update
apt install -y python-opengl python-numpy python-scipy
apt install -y libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libffi-dev

pip install --upgrade pip
pip install scipy numpy pyopengl ipython pillow
pip install pylint flake8
