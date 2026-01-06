#!/usr/bin/env python3
import gi
import sys
import os
import threading
import subprocess
import random
import base64
import pyotp
import qrcode
from io import BytesIO

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio, GdkPixbuf

action_file = os.path.dirname(os.path.abspath(__file__))+"/actions.py"
class MainWindow:
    def __init__(self, application):
        self.builder = Gtk.Builder()
        self.secret = self.generate_secret()

        # Import UI file:
        glade_file = (
            os.path.dirname(os.path.abspath(__file__)) + "/ui/MainWindow.ui"
        )

        self.builder.add_from_file(glade_file)
        self.application = application
        self.ui_window_main.set_application(application)

        self.ui_entry_secret.set_text(self.secret)

        # define button functions
        self.ui_button_remove.connect("clicked", self.on_remove_event)
        self.ui_button_help.connect("clicked", self.on_help_event)
        self.ui_button_change.connect("clicked", self.on_change_event)
        self.ui_entry_secret.connect("changed", self.on_entry_change)

        self.ui_window_main.show_all()

        sp = subprocess.run(["pkexec", action_file, "status"])
        if sp.returncode != 0:
            self.on_change_event(None)

########### button event functions ###########

    def on_remove_event(self, widget):
        subprocess.run(["pkexec", action_file, "remove"])
        self.apptication.quit()

    def on_help_event(self, widget):
        pass

    def on_change_event(self, widget):
        subprocess.run(["pkexec", action_file, "save", self.secret])
        self.ui_image_qr.set_from_pixbuf(self.get_qr_code(self.secret))
        self.ui_stack_main.set_visible_child_name("page_qr")
        self.ui_stack_buttons.set_visible_child_name("page_qr")
        self.ui_label_info.show()

    def on_entry_change(self, widget):
        try:
            # try decode
            base64.b32decode(widget.get_text())
            self.secret = widget.get_text()
            self.on_change_event(None)
        except:
            self.ui_image_qr.set_from_pixbuf(None)
            self.ui_label_info.hide()

########### helper functions ###########

    def generate_secret(self):
        random_bytes = os.urandom(10)
        return base64.b32encode(random_bytes).decode("utf-8")

    def __getattr__(self, name):
        # return object if exists
        if self.builder.get_object(name):
            return self.builder.get_object(name)

    def get_qr_code(self, secret):
        # Generate the QR code
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(os.environ["USER"]+"@etap", issuer_name="pardus-etap")
        qr = qrcode.make(uri+"&algorithm=SHA1&digits=6&period=30")

        # Convert QR code to a format that GTK can use
        with BytesIO() as output:
            qr.save(output, format="PNG")
            output.seek(0)
            # Create a Gio.MemoryInputStream from the BytesIO object
            memory_stream = Gio.MemoryInputStream.new_from_data(output.getvalue(), None)
            return GdkPixbuf.Pixbuf.new_from_stream(memory_stream, None)
        return None
