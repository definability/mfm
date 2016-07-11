OPERATION=$(tr [a-z] [A-Z] <<< ${1:-patch})

VERSION=$(python setup.py --version)

REGEX='^\([[:digit:]]\+\)\.\([[:digit:]]\+\)\.\([[:digit:]]\+\)$'

PATCH='echo "\1.\2.$((\3+1))"'
MINOR='echo "\1.$((\2+1)).0"'
MAJOR='echo "$((\1+1)).0.0"'

eval BUMPER='$'$OPERATION

NEW_VERSION=$(sed "s/${REGEX}/${BUMPER}/ge" <<< ${VERSION})

TIMESTAMP=$(date +%Y-%m-%d)
CHANGELOG_ENTRY="## [${NEW_VERSION}] - ${TIMESTAMP}"
sed -i "/^## \[Unreleased\]$/a\ \n${CHANGELOG_ENTRY}" CHANGELOG.md

CHANGELOG_HEAD_LINK="^\[Unreleased\]\(.*\)v${VERSION}...HEAD$"
CHANGELOG_NEW_HEAD_LINK="[Unreleased]\1v${NEW_VERSION}...HEAD"
CHANGELOG_NEW_COMPARISON="[${NEW_VERSION}]\1v${VERSION}...${NEW_VERSION}"
CHANGELOG_LINK="${CHANGELOG_NEW_HEAD_LINK}\n${CHANGELOG_NEW_COMPARISON}"
sed -i "s/${CHANGELOG_HEAD_LINK}/${CHANGELOG_LINK}/g" CHANGELOG.md
