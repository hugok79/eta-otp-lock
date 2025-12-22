#!/usr/bin/python3

import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from MainWindow import MainWindow

class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="tr.org.etap.otp-lock",
                         flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs
        )
        self.window = None
        GLib.set_prgname("tr.org.etap.otp-lock")

        self.add_main_option(
            "settings",
            ord("s"),
            GLib.OptionFlags(0),
            GLib.OptionArg(0),
            "Start settings page",
            None,
        )

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(self)
        else:
            self.window.present()


app = Application()
app.run(sys.argv)
