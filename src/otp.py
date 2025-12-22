#!/usr/bin/env python3
import gi
import pyotp
import time
import base64
import os
import qrcode
from io import BytesIO

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf, Gio


def generate_otp(random_bytes=None):
    if random_bytes is None:
        random_bytes = os.urandom(10)
    return base64.b32encode(random_bytes).decode("utf-8")

def update_otp(secret):
    try:
        return pyotp.TOTP(secret).now()
    except Exception as e:
        print(e)
        return "Invalid OTP"

def get_qr_code(secret):
    # Generate the QR code
    totp = pyotp.TOTP(secret.secret)
    uri = totp.provisioning_uri(secret.mail, issuer_name=secret.issuer)
    qr = qrcode.make(uri)

    # Convert QR code to a format that GTK can use
    with BytesIO() as output:
        qr.save(output, format="PNG")
        output.seek(0)
        # Create a Gio.MemoryInputStream from the BytesIO object
        memory_stream = Gio.MemoryInputStream.new_from_data(output.getvalue(), None)
        return GdkPixbuf.Pixbuf.new_from_stream(memory_stream, None)
    return None
