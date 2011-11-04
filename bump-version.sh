#!/bin/bash
#
# File: bump-version.sh
# Author: Einar Uvsløkk <einar.uvslokk@linux.com>
# Copyright: (c) 2011 Einar Uvsløkk
# License: GNU General Public License (GPL) version 3 or later
# Description: Bump the version number in autotools projects.
#
# This script assumes that version numbering is on the form
# 
#     major_version.minor_version.micro_version
#
# defined in the configure.ac script like this
#
#     m4_define(major_version, 0)
#     m4_define(minor_version, 1)
#     m4_define(micro_version, 0)
#     m4_define(version, major_version.minor_version.micro_version)

# some constants (modify per need)
TOPLEVEL_DIR="."
VERSION_FILE="${TOPLEVEL_DIR}/configure.ac"
PACKAGE_NAME="gengo"
PREFIX="m4_define(${PACKAGE_NAME}_"

usage()
{
	cat <<-EndUsage
	Usage: ${0} [options] [major.minor.micro]

	Available options:

	-h, --help     Show this help message and exit.
	-c, --current  Print the current version and exit.
	[-[-]]major    Only bump the current major version.
	[-[-]]minor    Only bump the current minor version.
	[-[-]]micro    Only bump the current micro version.

	Note that the flags listed above take precedence in the order they
	are listed, meaning that if any of these are supplied together with
	version numbers, the latter will be ignored.
	EndUsage
}

# get_current_version:
#
# Stores version number information in four different variables:
#
#     current_major      The major part of the version number
#     current_major      The minor part of the version number 
#     current_major      The micro part of the version number 
#     current_version    Dot separated representation of the version number
get_current_version()
{

	local tmp=$(grep "^${PREFIX}major" ${VERSION_FILE} | cut -d \( -f2)
	current_major="${tmp//[^0-9]/}"
	local tmp=$(grep "^${PREFIX}minor" ${VERSION_FILE} | cut -d \( -f2)
	current_minor="${tmp//[^0-9]/}"
	local tmp=$(grep "^${PREFIX}micro" ${VERSION_FILE} | cut -d \( -f2)
	current_micro="${tmp//[^0-9]/}"

	current_version=${current_major}.${current_minor}.${current_micro}
}

bump_major_version()
{
	sed -i -e "s/${PREFIX}major.*$/${PREFIX}major_version, $1\)/i" ${VERSION_FILE}
}

bump_minor_version()
{
	sed -i -e "s/${PREFIX}minor.*$/${PREFIX}minor_version, $1\)/i" ${VERSION_FILE}
}

bump_micro_version()
{
	sed -i -e "s/${PREFIX}micro.*$/${PREFIX}micro_version, $1\)/i" ${VERSION_FILE}
}

# We check for the help flag before testing the existence of the
# version file: ${TOPLEVEL_DIR}/${VERSION_FILE}
case ${1} in
	-h|--help) usage ; exit 0 ;;
esac

test -f ${VERSION_FILE} ||
{
	echo **Error**: Unable to locate version file: ${VERSION_FILE}.
	exit 1
}

get_current_version

case ${1} in
	-c|--current|current)
		echo ${current_version}
		exit 0 ;;
	major|-major|--major)
		bump_major_version $((current_major+1))
		exit 0 ;;
	minor|-minor|--minor)
		bump_minor_version $((current_minor+1))
		exit 0 ;;
	micro|-micro|--micro)
		bump_micro_version $((current_micro+1))
		exit 0 ;;
esac

# Assuming a custom version number is provided
if [[ ${1} != "" ]]; then
	tmp=${1}
	major=`echo ${1} | cut -d. -f1`
	minor=`echo ${1} | cut -d. -f2`
	micro=`echo ${1} | cut -d. -f3`

	# Perform some sanity checks to ensure we don't 
	# allow decrease the version number.
	if [[ ${major} -lt ${current_major} ]]; then
		echo -n "**Illegal bump** Decreasing major number: "
		echo    "${current_major} > ${major}"
		exit 1
	elif [[ ${minor} -lt ${current_minor} ]]; then
		echo -n "**Illegal bump** Decreasing minor number: "
		echo    "${current_minor} > ${minor}"
		exit 1
	elif [[ ${micro} -lt ${current_micro} ]]; then
		echo -n "**Illegal bump** Decreasing micro number: "
		echo    "${current_micro} > ${current_micro}"
		exit 1
	fi
	# Bump is okay!
	echo -n "Bumping ${PACKAGE_NAME} version: " 
	echo    "$current_version -> $major.$minor.$micro"
else
	cat <<-EndError
	Nothing to do!
	Run ${0} --help for more information
	EndError
fi

exit 0
