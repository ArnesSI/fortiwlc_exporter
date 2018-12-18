#!/bun/bash

# Check if we are on a tag (based on GitLab CI var or git describe)
if [ -z ${CI_TAG_REF+x} ] && ! git describe --exact-match 2>/dev/null; then
    # really not on a tag - append rev info to version
    VER_APPEND=$(git describe --tags | cut -d'-' -f 2-)
    bumpversion --no-commit --no-tag --allow-dirty --list --serialize "{major}.{minor}.{patch}-${VER_APPEND}" patch
fi
