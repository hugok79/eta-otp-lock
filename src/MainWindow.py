import sys
import gi
gi.require_version("Gtk", "3.0")

import otp

from gi.repository import Gtk, GLib

secret = "JBSWY3DPEHPK3PXP"

class MainWindow(object):
    def __init__(self, application=None):
        self.Application = application
        builder = Gtk.Builder.new_from_file(os.path.dirname(os.path.abspath(__file__))+"../ui/main.ui")
        win = builder.get_object("ui_main_window")
        self.msg = builder.get_object("ui_main_message")
        self.pin = builder.get_object("ui_main_pin")
        self.numpad = builder.get_object("ui_main_numpad")

        self.cur = ""

        if application:
            win.set_application(application)

        for i in range(0,10):
            but = builder.get_object(f"ui_main_n{i}")
            but.connect("clicked", self.num_event, str(i))

        delete = builder.get_object("ui_main_del")
        delete.connect("clicked", self.del_event)
        self.pin.set_text(self.format_cur())
        self.msg.set_text("")
        self.fail_count=0
        win.fullscreen()
        win.show_all()

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
