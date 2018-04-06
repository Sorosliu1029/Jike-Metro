# -*- coding: utf-8 -*-

"""
QR code that be scanned to allow login
"""

import qrcode
import tempfile
import webbrowser
from decimal import Decimal
from qrcode.image.svg import SvgImage
from PIL import Image

try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import qrcode.image.base

from jike.constants import JIKE_URI_SCHEME_FMT, RENDER2BROWSER_HTML_TEMPLATE


def make_qrcode(uuid, render_choice='browser'):
    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(JIKE_URI_SCHEME_FMT.format(**uuid))
    qr.make()

    render_choices = {
        'browser': render2browser,
        'terminal': render2terminal,
        'viewer': render2viewer
    }

    assert render_choice in render_choices, 'Unsupported render choice.\nAvailable choices: browser, viewer, terminal'
    render_choices[render_choice](qr)


def render2terminal(qr):
    qr.print_tty()


def render2browser(qr):
    img = qr.make_image(image_factory=JikeSvgPathImage)
    with tempfile.NamedTemporaryFile(suffix='.svg') as fp:
        img.save(fp)
        fp.seek(0)
        content = fp.read().decode('utf-8').splitlines()
    svg = content[1]
    assert svg.startswith('<svg') and svg.endswith('</svg>'), 'Render QR code fail'
    html = RENDER2BROWSER_HTML_TEMPLATE.substitute(qrcode_svg=svg)

    _, path = tempfile.mkstemp(suffix='.html')
    with open(path, 'wt', encoding='utf-8') as fp:
        fp.write(html)
    webbrowser.open('file://{}'.format(fp.name))


def render2viewer(qr):
    img = qr.make_image()
    _, path = tempfile.mkstemp(suffix='.png')
    with open(path, 'wb') as fp:
        img.save(fp)
    webbrowser.open('file://{}'.format(fp.name))


class JikeSvgPathImage(SvgImage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = []
        bg = Image.open('../docs/resources/guoguo3.jpg')
        width, height = bg.size
        step = width // 50
        for i in range(step // 2, width, step):
            for j in range(step // 2, width, step):
                color = bg.getpixel((i, j))
                self.colors.append('#{0:x}{1:x}{2:x}'.format(*color))

    def units(self, pixels, text=True):
        """
        A box_size of 10 (default) equals 3.3mm.
        """
        units = Decimal(pixels) / 3
        if not text:
            return units
        return '{}mm'.format(units)

    def _rect(self, row, col):
        x, y = self.pixel_box(row, col)[0]
        return ET.Element(
            'rect', x=self.units(x), y=self.units(y),
            width=self.unit_size, height=self.unit_size,
            fill=self.colors[row * 49 + col]
        )


if __name__ == '__main__':
    qr = qrcode.QRCode(
        version=8,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=4,
    )
    qr.add_data('Jike test')
    qr.make()
    img = qr.make_image(image_factory=JikeSvgPathImage)
    with tempfile.NamedTemporaryFile(suffix='.svg') as fp:
        img.save(fp)
        fp.seek(0)
        content = fp.read().decode('utf-8').splitlines()
    svg = '\n'.join(content)
    # assert svg.startswith('<svg') and svg.endswith('</svg>'), 'Render QR code fail'
    html = RENDER2BROWSER_HTML_TEMPLATE.substitute(qrcode_svg=svg)

    _, path = tempfile.mkstemp(suffix='.html')
    with open(path, 'wt', encoding='utf-8') as fp:
        fp.write(html)
    webbrowser.open('file://{}'.format(fp.name))
