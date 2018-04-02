import unittest
from collections import namedtuple
from jike.objects.wrapper import *


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.Test = namedtuple('Test', ['id', 'content', 'other', 'none'])

    def test_repr_namedtuple(self):
        self.Test.__repr__ = repr_namedtuple
        test = self.Test(**{'id': 'a', 'content': 'b', 'other': 'c', 'none': None})
        self.assertEqual(repr(test), 'Test(id=a, content=b)')

    def test_str_namedtuple(self):
        self.Test.__str__ = str_namedtuple
        test = self.Test(**{'id': 'a', 'content': 'b', 'other': 'c', 'none': None})
        self.assertEqual(str(test), 'Test(id=a, content=b, other=c)')

    def test_namedtuple_with_defaults(self):
        Test = namedtuple_with_defaults(self.Test)
        test = Test(**{'id': 'a', 'content': 'b', 'other': 'c'})
        self.assertEqual(test.id, 'a')
        self.assertEqual(test.content, 'b')
        self.assertEqual(test.other, 'c')
        self.assertIsNone(test.none)


if __name__ == '__main__':
    unittest.main()
