README
******

Gengo is a simple GObject generator written in python. It supports generating
GObject boilerplate code for the C programming language from the command-line
or from a Gtk interface.


Dependencies
============
Gengo uses the following software components:

- Python (http://www.pyhton.org)
- PyGObject (http://live.gnome.org/PyGObject)


Installation
============
Assuming dependencies are correctly installed, installing the application is
as simple as running the following command sequence from your favorite shell::

    ./autogen --prefix=/usr
    make
    sudo make install


Screenshots
===========
|general|

.. |general| image:: https://github.com/einaru/gengo/raw/master/data/gengo-general.png


Resources
=========
- Repository: https://github.com/einaru/gengo
- Issues:     https://github.com/einaru/gengo/issues


Copyright
=========
Copyright © 2011 Einar Uvsløkk <einar.uvslokk@linux.com>
Use of this application is granted under the terms of the GNU General Public
License (GPL) version 3 or later.
