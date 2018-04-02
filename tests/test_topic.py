import unittest
from jike.objects.topic import Topic


class TestTopic(unittest.TestCase):
    def test_topic(self):
        topic = Topic(**{'id': 'a', 'topicId': 'b'})
        self.assertEqual(topic.id, 'a')
        self.assertEqual(topic.topicId, 'b')
        self.assertIsNone(topic.topicType)


if __name__ == '__main__':
    unittest.main()
