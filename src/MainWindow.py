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

from gui import create_gui

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio, GdkPixbuf

action_file = os.path.dirname(os.path.abspath(__file__))+"/actions.py"
class MainWindow:
    def __init__(self, application):
        self.secret = self.generate_secret()

        create_gui(self)
        self.application = application
        self.ui_window_main.set_application(application)

        self.ui_button_newotp.connect("clicked", self.on_newotp_event)
        self.ui_button_show.connect("clicked", self.on_show_event)
        self.ui_button_delete.connect("clicked", self.on_delete_event)

        self.ui_window_main.show_all()

        self.ui_stack_main.set_visible_child_name("main")
        sp = subprocess.run(["pkexec", action_file, "status"])
        if sp.returncode != 0:
            self.ui_stack_main.set_visible_child_name("settings")

########### button event functions ###########

    def on_newotp_event(self, widget):
        self.secret = self.generate_secret()
        self.ui_stack_main.set_visible_child_name("settings")
        subprocess.run(["pkexec", action_file, "save", self.secret])

    def on_show_event(self, widget):
        self.update_qr()
        self.ui_stack_main.set_visible_child_name("qr")

    def on_delete_event(self, widget):
        self.ui_stack_main.set_visible_child_name("main")
        subprocess.run(["pkexec", action_file, "remove"])


########### helper functions ###########

    def update_qr(self):
        self.ui_label_secret.set_text(self.secret)
        self.ui_image_qr.set_from_pixbuf(self.get_qr_code(self.secret))

    def generate_secret(self):
        random_bytes = os.urandom(10)
        return base64.b32encode(random_bytes).decode("utf-8")

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
