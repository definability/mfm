[![Build Status](https://travis-ci.org/char-lie/mfm.svg?branch=master)](https://travis-ci.org/char-lie/mfm)
[![Coverage Status](https://coveralls.io/repos/github/char-lie/mfm/badge.svg?branch=master)](https://coveralls.io/github/char-lie/mfm?branch=master)

# Morphable Face Model

Data used in this example should be downloaded from the
[official site](http://faces.cs.unibas.ch/bfm/main.php?nav=1-1-0&id=details)
of University of Basel.

Morphable face model described in the following
[article](http://gravis.cs.unibas.ch/publications/2009/BFModel09.pdf):

> Paysan P.,Knothe R., Amberg B., Romdhani S., and Vetter T.
> "A 3D Face Model for Pose and Illumination Invariant Face Recognition".
> Proceedings of the 6th IEEE International Conference
>   on Advanced Video and Signal based Surveillance (AVSS) for Security,
>   Safety and Monitoring in Smart Environments Genova (Italy),
>   pp 296 - 301, September, 2009

# Development

Run the Docker container with Python
```bash
xhost +
docker run --rm -it -v $PWD:/src/ \
           -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
           --device=/dev/dri/card0:/dev/dri/card0 python:3 bash
```

Install needed packages
```bash
apt update
apt install -y python-opengl python-numpy python-scipy

pip install --upgrade pip
pip install scipy numpy pyopengl ipython pillow

apt install xserver-xorg-video-dummy
curl http://xpra.org/xorg.conf -o /usr/share/X11/xorg.conf.d/xorg.conf
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./10.log -config ./xorg.conf :10
export DISPLAY=:10
```

http://askubuntu.com/questions/453109/add-fake-display-when-no-monitor-is-plugged-in
https://xpra.org/trac/wiki/Xdummy

