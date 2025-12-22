
import os, sys
import random
import otp

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

secret = None
secret_file = "{}/.config/pardus/otp".format(os.environ["HOME"])
if os.path.isfile(secret_file):
    with open(secret_file, "r") as f:
        secret = f.read()

if secret is None:
    secret = otp.generate_seed(15)

class MainWindow(object):
    def __init__(self, application=None):
        self.Application = application
        builder = Gtk.Builder.new_from_file(os.path.dirname(os.path.abspath(__file__))+"/../ui/main.ui")
        self.win = builder.get_object("ui_main_window")
        stack = builder.get_object("ui_main_stack")
        self.msg = builder.get_object("ui_main_message")
        self.pin = builder.get_object("ui_main_pin")
        self.numpad = builder.get_object("ui_main_numpad")

        self.cur = ""

        if application:
            self.win.set_application(application)

        for i in range(0,10):
            but = builder.get_object(f"ui_main_n{i}")
            but.connect("clicked", self.num_event, str(i))

        delete = builder.get_object("ui_main_del")
        delete.connect("clicked", self.del_event)
        self.pin.set_text(self.format_cur())
        self.msg.set_text("")
        self.fail_count=0

        self.qr = builder.get_object("ui_settings_qr")
        self.secret_entry = builder.get_object("ui_settings_secret")
        self.secret_entry.connect("changed", self.secret_change)
        self.secret_entry.set_text(str(secret))

        but_random = builder.get_object("ui_settings_random")
        but_random.connect("clicked", self.random_seed_event)

        but_save = builder.get_object("ui_settings_save")
        but_save.connect("clicked", self.save_event)


        self.win.show_all()
        self.win.connect("destroy", Gtk.main_quit)

        if secret is None or "--settings" in sys.argv:
            builder.get_object("ui_box_main").hide()
            stack.set_visible_child_name("settings")
            self.win.resize(1,1)
        else:
            stack.set_visible_child_name("main")
            self.win.fullscreen()

    def random_seed_event(self, widget):
        self.secret_entry.set_text(otp.generate_seed(15))

    def save_event(self, widget):
        with open(secret_file, "w") as f:
            f.write(self.secret_entry.get_text())
            f.flush()
        sys.exit(0)

    def secret_change(self, entry):
        print(entry.get_text())
        secret = otp.Secret(otp.generate_otp(entry.get_text().encode("utf-8")), "etap", "etap")
        self.qr.set_from_pixbuf(otp.get_qr_code(secret))
        self.win.resize(1,1)


    def check(self):
        cur = otp.update_otp(secret)
        print(cur, self.cur)
        if str(cur) == str(self.cur):
            sys.exit(0)
        self.cur = ""
        self.pin.set_text(self.format_cur())
        self.numpad.set_sensitive(True)
        self.fail_count+=1
        self.msg.set_text(f"Login failed ({self.fail_count})")

    def format_cur(self):
        cur = (6-len(self.cur))*"-"+self.cur
        return cur[:3]+" "+ cur[3:]

    def num_event(self, widget, i):
        self.cur += i
        self.pin.set_text(self.format_cur())
        if len(self.cur) == 6:
            self.numpad.set_sensitive(False)
            GLib.timeout_add(2000, self.check)


    def del_event(self,widget):
        self.cur = self.cur[:-1]
        self.pin.set_text(self.format_cur())

if __name__ == "__main__":
    main = MainWindow()
    Gtk.main()
