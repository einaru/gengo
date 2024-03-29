#!/bin/sh
# Run this to generate all the initial makefiles, etc.

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

PKG_NAME="gengo"

(test -f $srcdir/configure.ac \
  && test -f $srcdir/autogen.sh \
  && test -d $srcdir/ggo) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
    echo " top-level $PKG_NAME directory"
    exit 1
}

DIE=0

if ! which gnome-autogen.sh ; then
  echo "You need to install the gnome-common module and make"
  echo "sure the gnome-autogen.sh script is in your \$PATH."
  exit 1
fi

USE_GNOME2_MACROS=1 . gnome-autogen.sh
