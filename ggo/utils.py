# -*- coding: utf-8 -*-
"""
File: gengobject.py
Author: Einar Uvsløkk <einar.uvslokk@linux.com>
License: GNU General Public License (GPL) version 3 or later
Description: Utility module for the Gengo GObject generator.
"""
import os


class FileExistsError(Exception):
    def __init__(self, *args, **kwargs):
        super(FileExistsError, self).__init__(*args, **kwargs)


class Attributes(dict):
    def __init__(self, *args, **kwargs):
        super(Attributes, self).__init__(*args, **kwargs)
        self.__dict__ = self


def split_camel_case(string):
    """Splits a camel cased string into a list of words.

    >>> split_camel_case("YouAreTheMan")
    ['You', 'Are', 'The', 'Man']

    Args:
        string (str): a camel cased string.

    Returns:
        a list of capitalized words.
    """
    L, lower = [], False
    for token in string:
        if token.isupper() and lower:
            L.append(" ")
        lower = not token.isupper()
        L.append(token)
    return "".join(L).split(" ")


def write_file(filename, content, overwrite=True):
    """Writes some content to file.

    Args:
        filename (str): The name of the file to write content to.
            Will be written to current working directory if just the
            basename is privided.
        content (str): The content to be written to file.
        overwrite (bool): Whether or not to check if the file already
            exists.

    Raises:
        FileExistsError: Rasied if called with the overwrite
            flag enabled and the file already exists.
    """
    if not overwrite:
        if os.path.isfile(filename):
            msg = str_on_file_exists.format(filename=filename)
            raise FileExistsError(msg)
        else:
            overwrite = True

    if overwrite:
        with open(filename, "w") as f:
            f.write(content)

    return True


# The following strings are translateable string commonly used in both 
# the CLI and th Gtk frontend.
str_on_file_exists = _("{filename} already exists.")
str_on_file_overwrite = _("Do you want to overwrite?")
