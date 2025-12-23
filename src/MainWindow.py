import os, sys
import random
import otp

import utils

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

secret_len = 40
secret_file = "{}/.config/pardus/otp".format(os.environ["HOME"])
class MainWindow(object):
    def init_secret(self):
        self.secret = None
        if os.path.isfile(secret_file):
            with open(secret_file, "rb") as f:
                self.secret = f.read()

        if self.secret is None:
            self.secret = os.urandom(secret_len)



    def __init__(self, application=None):
        self.Application = application
        builder = Gtk.Builder.new_from_file(os.path.dirname(os.path.abspath(__file__))+"/../ui/main.ui")
        self.win = builder.get_object("ui_main_window")
        stack = builder.get_object("ui_main_stack")
        self.msg = builder.get_object("ui_main_message")
        self.pin = builder.get_object("ui_main_pin")
        self.numpad = builder.get_object("ui_main_numpad")

        self.cur = ""
        self.init_secret()

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

        but_random = builder.get_object("ui_settings_random")
        but_random.connect("clicked", self.random_seed_event)

        but_save = builder.get_object("ui_settings_save")
        but_save.connect("clicked", self.save_event)

        but_import = builder.get_object("ui_settings_import")
        but_import.connect("clicked", self.import_event)

        but_export = builder.get_object("ui_settings_export")
        but_export.connect("clicked", self.export_event)


        self.win.show_all()
        self.win.connect("destroy", Gtk.main_quit)

        if self.secret is None or "--settings" in sys.argv:
            builder.get_object("ui_box_main").hide()
            stack.set_visible_child_name("settings")
            self.win.set_resizable(False)
            self.win.resize(1,1)
            self.secret_change(self.secret)
        else:
            stack.set_visible_child_name("main")
            self.win.fullscreen()

    def random_seed_event(self, widget):
        self.secret_change(os.urandom(secret_len))

    def save_event(self, widget):
        with open(secret_file, "wb") as f:
            f.write(self.secret)
            f.flush()
        if widget:
            Gtk.main_quit()

    def import_event(self, widget):
        file = utils.select_file()
        if file:
            with open(file, "rb") as f:
                self.secret = f.read()
                if len(self.secret) > secret_len:
                    self.secret = self.secret[:secret_len]
                print(self.secret)
            self.save_event(None)

    def export_event(self, widget):
        file = utils.save_file()
        if file:
            with open(file, "wb") as f:
                f.write(self.secret)
                f.flush()


    def secret_change(self, new_secret):
        self.secret = new_secret
        secret = otp.Secret(otp.generate_otp(new_secret), "etap", "etap")
        self.qr.set_from_pixbuf(otp.get_qr_code(secret))
        self.win.resize(1,1)

    def check(self):
        secret = otp.generate_otp(self.secret.encode("utf-8"))
        cur = otp.update_otp(secret)
        print(cur, self.cur, self.secret, secret)
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
