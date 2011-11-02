AC_INIT([gengo], [0.1], [einar.uvslokk@linux.com])

AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([2.6])

PYGOBJECT_REQUIRED_VERSION=2.90.0

PKG_CHECK_MODULES([PYGOBJECT3],
				  [pygobject-3.0 >= $PYGOBJECT_REQUIRED_VERSION)],,
				  [PKG_CHECK_MODULES([PYGOBJECT2], [pygobject-2.0 >= 2.28.0])])

IT_PROG_INTLTOOL([0.40.0])
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION([0.17])
GETTEXT_PACKAGE=gengo
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [GETTEXT package name])

AS_AC_EXPAND(DATADIR, "${datadir}")
AS_AC_EXPAND(PKGDATADIR, "${datadir}/${PACKAGE}")
AS_AC_EXPAND(LOCALEDIR, "${localedir}")

AC_CONFIG_FILES([
po/Makefile.in
Makefile
data/Makefile
ggo/defs.py
])

AC_OUTPUT

echo "
	Configuration:
	
	Source code location ........: ${src_dir}
	Installation prefx ..........: ${prefix}
"
