#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

set -e "${VERBOSE:+-x}"

ROOT_PATH=$(rpm --eval %_topdir)
RPMSRC_PATH=$(rpm --eval %_sourcedir)
BUILD_PATH=$(rpm --eval %_builddir)
SPECS_PATH=$(rpm --eval %_specdir)

# Create rpmbuild dirs
#mkdir -p $ROOT_PATH/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

# Clean build dirs (do not clean $ROOT_PATH/*RPMS)
#rm -rf $ROOT_PATH/{BUILD,BUILDROOT,SOURCES,SPECS}/*

# Guess the pkg name
SPEC_FILE=`ls *.spec`
PKG_NAME=$(rpmspec --srpm -q --queryformat='%{name}' $SPEC_FILE)

# Python: generate tarball
yum install -y python34-setuptools
python3 setup.py sdist

# Install build dependencies
yum-builddep -y ${SPEC_FILE} || exit 1

# List and download sources
spectool ${SPEC_FILE}
spectool -g -R ${SPEC_FILE} || exit 1

# Copy extra files (eval by rpm to ensure macros are expanded)
EVALSPEC=$(rpmspec -P $SPEC_FILE)
for i in $(echo "$EVALSPEC" | grep '^Source.*:' | awk '{print $2}') \
         $(echo "$EVALSPEC" | grep '^Patch.*:' | awk '{print $2}'); do
    for j in $i $(basename $i); do
        [ -f $j ] && cp -f $j $RPMSRC_PATH && break
    done
done
cp -f $SPEC_FILE $SPECS_PATH

# Build RPM package (but dont build debuginfo package)
rpmbuild -ba $SPECS_PATH/$SPEC_FILE --define "debug_package %{nil}" --define "_rpmdir $(pwd)/rpms" --define "_srcrpmdir $(pwd)/srpms"
