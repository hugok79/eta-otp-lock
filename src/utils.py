import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def select_file():
    dialog = Gtk.FileChooserDialog(
        title="Select a File",
        action=Gtk.FileChooserAction.OPEN)
    dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
    )
    response = dialog.run()
    ret = None
    if response == Gtk.ResponseType.OK:
        ret = dialog.get_filename()
    dialog.destroy()
    return ret

def save_file():
    dialog = Gtk.FileChooserDialog(
        title="Save a File",
        action=Gtk.FileChooserAction.SAVE)
    dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
    )
    response = dialog.run()
    ret = None
    if response == Gtk.ResponseType.OK:
        ret = dialog.get_filename()
    dialog.destroy()
    return ret
