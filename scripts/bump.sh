VERSION=$(python setup.py --version)

REGEX='^\([[:digit:]]\+\)\.\([[:digit:]]\+\)\.\([[:digit:]]\+\)$'

PATCH='echo "\1.\2.$((\3+1))"'
MINOR='echo "\1.$((\2+1)).0"'
MAJOR='echo "$((\1+1)).0.0"'
