import qrcode
import unittest
from unittest.mock import *

from jike import qr_code


class TestJikeQrCode(unittest.TestCase):
    def setUp(self):
        self.qr = qrcode.QRCode()
        self.qr.add_data('JikeMetro')

    def test_make_qrcode(self):
        with patch('jike.qr_code.render2terminal', return_value=None), \
             patch('jike.qr_code.render2browser', return_value=None), \
             patch('jike.qr_code.render2viewer', return_value=None):
            result = qr_code.make_qrcode({'uuid': '123'})
        self.assertIsNone(result)

        with patch('jike.qr_code.render2terminal', return_value=None), \
             patch('jike.qr_code.render2browser', return_value=None), \
             patch('jike.qr_code.render2viewer', return_value=None), \
             self.assertRaises(AssertionError):
            qr_code.make_qrcode({'uuid': '123'}, render_choice='illegal choice')

    @patch.object(qrcode.QRCode, 'print_tty')
    def test_render2terminal(self, mock_print_tty):
        result = qr_code.render2terminal(self.qr)
        self.assertIsNone(result)
        mock_print_tty.assert_called_once()

    def test_render2browser(self):
        m = mock_open()
        with patch('tempfile.mkstemp', return_value=(None, 'a.html')), \
             patch('builtins.open', m), \
             patch('webbrowser.open', return_value=None):
            result = qr_code.render2browser(self.qr)
        self.assertIsNone(result)
        m.assert_called_once_with('a.html', 'wt', encoding='utf-8')
        m().write.assert_called()

    def test_render2viewer(self):
        m = mock_open()
        with patch('tempfile.mkstemp', return_value=(None, 'a.png')), \
             patch('builtins.open', m), \
             patch('webbrowser.open', return_value=None):
            result = qr_code.render2viewer(self.qr)
        self.assertIsNone(result)
        m.assert_called_once_with('a.png', 'wb')
        m().write.assert_called()


if __name__ == '__main__':
    unittest.main()
