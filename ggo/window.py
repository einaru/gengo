# -*- coding: utf-8 -*-
"""
File: window.py
Author: Einar Uvsløkk <einar.uvslokk@linux.com>
License: GNU General Public License (GPL) version 3 or later
Description: Gtk frontend for the Gengo GObject generator.
"""
import os

from gi.repository import Gtk, GLib, Gio

import ggo
from ggo import templates, licenses, utils


def get_user_name():
    name = GLib.get_real_name()
    if name == "":
        name = GLib.get_user_name()
    return name


def get_user_email():
    return "{}@{}".format(GLib.get_user_name(), GLib.get_host_name())


def run_error_dialog(error, question, parent):
    dialog = Gtk.Dialog("Error",
                        parent,
                        Gtk.DialogFlags.DESTROY_WITH_PARENT,
                        (Gtk.STOCK_YES, Gtk.ResponseType.YES,
                         Gtk.STOCK_NO, Gtk.ResponseType.NO))
    content_area = dialog.get_content_area()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    box.set_border_width(12)
    content_area.pack_start(box, False, False, 0)
    box.pack_start(Gtk.Image(stock=Gtk.STOCK_DIALOG_ERROR,
                   icon_size=Gtk.IconSize.DIALOG), False, False, 0)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    box.pack_start(vbox, False, False, 0)
    vbox.pack_start(Gtk.Label(error), False, False, 0)
    vbox.pack_start(Gtk.Label(question), False, False, 0)
    box.show_all()
    retval = dialog.run() == Gtk.ResponseType.YES
    dialog.destroy()
    return retval


UI_FILE = "window.ui"
OBJECTS = ["ActionGroup", "Box"]


class GengoWindow(Gtk.Window):
    __gtype_name__ = "GengoWindow"

    def __init__(self, *args, **kwargs):
        super(GengoWindow, self).__init__(*args, **kwargs)
        self.attr = utils.Attributes()

        assert(os.path.exists(ggo.PKG_DATA_DIR))

        filename = os.path.join(ggo.PKG_DATA_DIR, UI_FILE)
        self.ui = Gtk.Builder()
        self.ui.add_objects_from_file(filename, OBJECTS)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.INFO)
        self.infobar.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        label = Gtk.Label("")
        self.infobar.get_content_area().pack_start(label, False, False, 0)
        label.show_all()
        self.infobar.set_no_show_all(True)
        self.infobar.connect("response", self.on_info_response)

        box.pack_start(self.infobar, False, False, 0)

        box.pack_start(self.ui.get_object("Box"), True, False, 0)

        self.init_widgets()

        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("applications-development")
        self.set_title("Gengo - GObject Generator")

        self.ui.connect_signals(self)
        self.connect("destroy", self.on_destroy)

    def init_widgets(self):
        self.ui.get_object("Author").set_text(get_user_name())
        self.ui.get_object("Email").set_text(get_user_email())
        self.ui.get_object("FileChooserButton").set_current_folder(os.getcwd())
        self.ui.get_object("ClassName").grab_focus()

        self.ui.get_object("Licenses").set_entry_text_column(0)
        self.ui.get_object("Licenses").set_id_column(1)
        for _id, license in sorted(licenses.Licenses.iteritems()):
            self.ui.get_object("Licenses").append(_id, license[0])
        self.ui.get_object("Licenses").insert(0, "NONE", "NONE")
        self.ui.get_object("Licenses").set_active(0)

    def on_destroy(self, widget, data=None):
        Gtk.main_quit()

    def on_help_activate(self, action, data=None):
        pass

    def on_info_response(self, widget, response):
        widget.hide()

    def on_generate_activate(self, action, data=None):
        """Callback for the Generate button.

        Fills the blanks in the template strings and writes template
        strings to file.
        """
        license, prefix, files = "", _("Successfully created:"), []

        license_id = self.ui.get_object("Licenses").get_active_id()
        print license_id
        if not license_id == "NONE":
            license = licenses.Licenses[license_id][1]

        self.attr.author = self.ui.get_object("Author").get_text()
        self.attr.email = self.ui.get_object("Email").get_text()

        # Create the header file
        content_h = templates.HEADER.format(license=license, **self.attr)
        content_c = templates.SOURCE.format(license=license, **self.attr)

        bundle = [(self.filename_h, content_h), (self.filename_c, content_c)]
        for filename, content in bundle:
            try:
                success = False
                success = utils.write_file(filename, content, False)
            except utils.FileExistsError as e:
                if run_error_dialog(str(e), utils.str_on_file_overwrite, self):
                    success = utils.write_file(filename, content, True)

            if success:
                files.append(filename)
                self.show_message("{} {}".format(prefix, ", ".join(files)))

    def on_class_name_changed(self, widget, data=None):
        """Callback for the ClassName entry widget.

        Updates the sensitivity state of the Generate button, and
        creates and sets various attributes based on the input.
        """
        text = widget.get_text()
        self.ui.get_object("Generate").set_sensitive(text != "")

        if text != "":
            self.set_attributes(utils.split_camel_case(text))

            self.ui.get_object("Namespace").set_text(self.attr.uc_prefix)
            self.ui.get_object("Type").set_text(self.attr.uc_suffix)
            self.ui.get_object("HeaderFile").set_text(self.filename_h)
            self.ui.get_object("SourceFile").set_text(self.filename_c)

    def show_message(self, message):
        self.infobar.get_content_area().get_children()[0].set_text(message)
        self.infobar.show()

    def set_attributes(self, words):
        """Sets the various attributes required by the templates."""
        self.attr.cc = "".join(words)
        self.attr.cc_prefix = words[0]
        self.attr.lc = "_".join(words).lower()
        self.attr.uc = "_".join(words).upper()
        self.attr.uc_prefix = words[0].upper()
        self.attr.uc_suffix = "_".join(words[1:]).upper()
        self.attr.filename = "-".join(words).lower()
        self.filename_h = self.attr.filename + ".h"
        self.filename_c = self.attr.filename + ".c"


class GengoApplication(Gtk.Application):
    """Implmentation of a Gtk.Application just for the fun of it."""
    __gtype_name__ = "GengoApplication"

    def __init__(self, *args, **kwargs):
        super(GengoApplication, self).__init__(*args, **kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, data=None):
        window = GengoWindow()
        window.show_all()
        window.set_application(self)
        self.add_window(window)


def main():
    app = GengoApplication(application_id="org.gnome.gengo")
    return app.run(None)
