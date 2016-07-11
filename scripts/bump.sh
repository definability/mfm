OPERATION=$(tr [a-z] [A-Z] <<< ${1:-patch})

VERSION=$(python setup.py --version)

REGEX='^\([[:digit:]]\+\)\.\([[:digit:]]\+\)\.\([[:digit:]]\+\)$'

PATCH='echo "\1.\2.$((\3+1))"'
MINOR='echo "\1.$((\2+1)).0"'
MAJOR='echo "$((\1+1)).0.0"'

eval BUMPER='$'$OPERATION

NEW_VERSION=$(sed "s/${REGEX}/${BUMPER}/ge" <<< ${VERSION})
