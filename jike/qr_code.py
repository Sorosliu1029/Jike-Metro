# -*- coding: utf-8 -*-

"""
QR code that be scanned to allow login
"""

import qrcode
import tempfile
import webbrowser
from .constants import JIKE_URI_SCHEME_FMT


def make_qrcode(uuid):
    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(JIKE_URI_SCHEME_FMT.format(**uuid))
    img = qr.make_image()
    _, path = tempfile.mkstemp(suffix='.png')
    with open(path, 'wb') as fp:
        img.save(fp)
    webbrowser.open(f'file://{fp.name}')
