dnl Process this file with autoconf to produce a configure script.

m4_define(gengo_major_version, 0)
m4_define(gengo_minor_version, 1)
m4_define(gengo_micro_version, 0)
m4_define(gengo_version,
		  gengo_major_version.gengo_minor_version.gengo_micro_version)

AC_INIT([gengo], [gengo_version], [https://github.com/einaru/gengo/issues],
		[gengo], [https://github.com/einaru/gengo])

AC_DEFINE(GENGO_MAJOR_VERSION, gengo_major_version, [Gengo major version])
AC_SUBST(GENGO_MAJOR_VERSION,  gengo_major_version)
AC_DEFINE(GENGO_MINOR_VERSION, gengo_minor_version, [Gengo minor version])
AC_SUBST(GENGO_MINOR_VERSION,  gengo_minor_version)
AC_DEFINE(GENGO_MICRO_VERSION, gengo_micro_version, [Gengo micro version])
AC_SUBST(GENGO_MICRO_VERSION,  gengo_micro_version)

AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([2.7])

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
