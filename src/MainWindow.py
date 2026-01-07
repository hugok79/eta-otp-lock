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
        self.ui_button_import.connect("clicked", self.on_import_event)
        self.ui_button_delete.connect("clicked", self.on_delete_event)
        self.ui_button_fromkey.connect("clicked", self.on_fromkey_event)

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

    def on_fromkey_event(self, widget):
        secret = self.input_secret()
        if secret:
            if self.is_base32(secret):
                self.secret = secret
            else:
                self.secret = self.generate_secret(secret.encode("utf-8"))
            self.ui_stack_main.set_visible_child_name("settings")
            subprocess.run(["pkexec", action_file, "save", self.secret])

    def on_import_event(self, widget):
        filename = self.open_file()
        if filename:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                self.secret = base64.b32encode(data).decode("utf-8")
            self.ui_stack_main.set_visible_child_name("settings")
            subprocess.run(["pkexec", action_file, "save", self.secret])

    def on_export_event(self, widget):
        filename = self.save_file()
        if filename:
            with open(filename, "wb") as f:
                data = base64.b32decode(self.secret.encode("utf-8"))
                pickle.dump(data, file=f)


########### helper functions ###########

    def update_qr(self):
        self.ui_label_secret.set_text(self.secret)
        self.ui_image_qr.set_from_pixbuf(self.get_qr_code(self.secret))

    def generate_secret(self, random_bytes = None):
        if random_bytes is None:
            random_bytes = os.urandom(10)
        return base64.b32encode(random_bytes).decode("utf-8")

    def is_base32(self, data):
        try:
            base64.b32decode(data)
            return True
        except:
            return False

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

########### file pick / save functions ###########

    def open_file(self):
        dialog = Gtk.FileChooserDialog(
            title="Select a File",
            parent=self.ui_window_main,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = dialog.run()
        filename = None
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        dialog.destroy()
        return filename

    def save_file(self):
        dialog = Gtk.FileChooserDialog(
            title="Save a File",
            parent=self.ui_window_main,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        response = dialog.run()
        filename = None
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        dialog.destroy()
        return filename

    def input_secret(self):
        dialog = Gtk.Dialog(
            title="Enter a Secret",
            parent=self.ui_window_main
        )
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        dialog.get_content_area().add(box)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter your secret here")
        box.pack_start(entry, True, True, 0)

        dialog.show_all()
        response = dialog.run()

        # Check the response
        user_input = None
        if response == Gtk.ResponseType.OK:
            user_input = entry.get_text()
        dialog.destroy()
        return user_input
