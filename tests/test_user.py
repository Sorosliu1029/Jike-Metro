import unittest
from jike.objects.user import User


class TestUser(unittest.TestCase):
    def test_user(self):
        user = User(**{'id': 'a', 'userId': 'b'})
        self.assertEqual(user.id, 'a')
        self.assertEqual(user.userId, 'b')
        self.assertIsNone(user.username)


if __name__ == '__main__':
    unittest.main()
