import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def create_gui(self):
########## Main widgets ##########
        self.ui_window_main = Gtk.Window()

        self.ui_stack_main = Gtk.Stack()

        box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box1.pack_start(Gtk.Label(), True, True, 0)
        box1.pack_start(box2, True, True, 0)
        box1.pack_start(Gtk.Label(), True, True, 0)

        box2.pack_start(Gtk.Label(), True, True, 0)
        box2.pack_start(self.ui_stack_main, True, True, 0)
        box2.pack_start(Gtk.Label(), True, True, 0)

        self.ui_window_main.add(box1)
        self.ui_window_main.set_resizable(False)
        self.ui_window_main.set_size_request(400,400)

########## Otp create page ##########

        self.ui_box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.ui_box_main.set_spacing(8)
        self.ui_stack_main.add_named(self.ui_box_main, "main")

        self.ui_box_main.pack_start(Gtk.Label(label="Hali hazırda oluşturulmuş\nbir OTP bulunmamaktadır."), False, False, 0)

        self.ui_button_newotp = Gtk.Button(label="Yeni OTP oluştur")
        self.ui_box_main.pack_start(self.ui_button_newotp, False, False, 0)

        self.ui_button_import = Gtk.Button(label="OTP dosyasını içe aktar")
        self.ui_box_main.pack_start(self.ui_button_import, False, False, 0)


        self.ui_button_fromkey = Gtk.Button(label="Anahtar ile oluştur")
        self.ui_box_main.pack_start(self.ui_button_fromkey, False, False, 0)

########## Otp settings page ##########

        self.ui_box_settings = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.ui_box_settings.set_spacing(8)
        self.ui_stack_main.add_named(self.ui_box_settings, "settings")

        self.ui_box_settings.pack_start(Gtk.Label(label="Kullanıcınıza ait\nbir OTP bulunmaktadır."), False, False, 0)

        self.ui_button_show = Gtk.Button(label="QR / Anahtar Göster")
        self.ui_box_settings.pack_start(self.ui_button_show, False, False, 0)

        self.ui_button_export = Gtk.Button(label="OTP dosyasını dışa aktar")
        self.ui_box_settings.pack_start(self.ui_button_export, False, False, 0)

        self.ui_button_delete = Gtk.Button(label="OTP Sil")
        self.ui_box_settings.pack_start(self.ui_button_delete, False, False, 0)

########## QR / Key page ##########

        self.ui_box_qr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.ui_box_qr.set_spacing(8)
        self.ui_stack_main.add_named(self.ui_box_qr, "qr")

        self.ui_image_qr = Gtk.Image()
        self.ui_image_qr.set_pixel_size(256)
        self.ui_image_qr.set_from_icon_name("image-missing", 0)
        self.ui_box_qr.pack_start(self.ui_image_qr, True, True, 0)

        self.ui_label_secret = Gtk.Label(label="JBSWY3DPEHPK3PXP")
        self.ui_box_qr.pack_start(self.ui_label_secret, False, False, 0)



