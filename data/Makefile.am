guidir = $(pkgdatadir)
gui_DATA = \
        window.ui

desktop_in_files = gengo.desktop.in
desktopdir = $(datadir)/applications
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST = \
	$(gui_DATA) \
	$(desktop_in_files)

CLEANFILES = \
	$(desktop_DATA)


-include $(top_srcdir)/git.mk
