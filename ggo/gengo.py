#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: gengo
Author: Einar Uvsløkk <einar.uvslokk@linux.com>
License: GNU General Public License (GPL) version 3 or later
Description: CLI frontend for the Gengo GObject generator.
"""
import os
import sys
import optparse

import templates
import utils


def create_gobject_files(classname, author, email, no_license=False):
    if no_license:
        license = ""
    else:
        license = templates.LICENSE_GPL

    attr = utils.Attributes()
    words = utils.split_camel_case(classname)

    attr.cc = classname
    attr.cc_prefix = "".join(words[1:])
    attr.lc = "_".join(words).lower()
    attr.uc = "_".join(words).upper()
    attr.uc_prefix = words[0].upper()
    attr.uc_suffix = "_".join(words[1:]).upper()
    attr.filename = "-".join(words).lower()
    attr.author = author
    attr.email = email

    filename_h = attr.filename + ".h"
    filename_c = attr.filename + ".c"

    content_h = templates.HEADER.format(license=license, **attr)
    content_c = templates.SOURCE.format(license=license, **attr)

    bundle = [(filename_h, content_h), (filename_c, content_c)]
    for filename, content in bundle:
        try:
            utils.write_file(filename, content, False)
        except utils.FileExistsError as e:
            print >> sys.stderr, format(e)
            print >> sys.stdout, utils.str_on_file_overwrite,
            answer = raw_input(_("[y|n]"))
            if answer in ["y", "Y", "yes", "YES", "Yes"]:
                utils.write_file(filename, content, True)
