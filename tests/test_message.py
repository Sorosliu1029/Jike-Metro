import unittest
from jike.objects.message import *


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.message = {'id': 'a', 'content': 'b'}

    def test_official_message(self):
        message = {'video': 'c'}
        message.update(self.message)
        official_message = OfficialMessage(**message)
        self.assertEqual(official_message.id, 'a')
        self.assertEqual(official_message.content, 'b')
        self.assertEqual(official_message.video, 'c')
        self.assertIsNone(official_message.type)

    def test_original_post(self):
        message = {'messageId': 'c'}
        message.update(self.message)
        original_post = OriginalPost(**message)
        self.assertEqual(original_post.id, 'a')
        self.assertEqual(original_post.content, 'b')
        self.assertEqual(original_post.messageId, 'c')
        self.assertIsNone(original_post.type)

    def test_repost(self):
        message = {'replyToComment': 'c'}
        message.update(self.message)
        repost = Repost(**message)
        self.assertEqual(repost.id, 'a')
        self.assertEqual(repost.content, 'b')
        self.assertEqual(repost.replyToComment, 'c')
        self.assertIsNone(repost.type)

    def test_question(self):
        message = {'title': 'c'}
        message.update(self.message)
        question = Question(**message)
        self.assertEqual(question.id, 'a')
        self.assertEqual(question.content, 'b')
        self.assertEqual(question.title, 'c')
        self.assertIsNone(question.type)

    def test_answer(self):
        message = {'question': 'c'}
        message.update(self.message)
        answer = Answer(**message)
        self.assertEqual(answer.id, 'a')
        self.assertEqual(answer.content, 'b')
        self.assertEqual(answer.question, 'c')
        self.assertIsNone(answer.type)

    def test_person_update_section(self):
        personal_update_section = PersonalUpdateSection(**{'id': 'a', 'items': 'b'})
        self.assertEqual(personal_update_section.id, 'a')
        self.assertEqual(personal_update_section.items, 'b')
        self.assertIsNone(personal_update_section.type)

    def test_personal_update(self):
        personal_update = PersonalUpdate(**{'id': 'a', 'action': 'b'})
        self.assertEqual(personal_update.id, 'a')
        self.assertEqual(personal_update.action, 'b')
        self.assertIsNone(personal_update.type)

    def test_comment(self):
        comment = Comment(**{'id': 'a', 'content': 'b', 'liked': True})
        self.assertEqual(comment.id, 'a')
        self.assertEqual(comment.content, 'b')
        self.assertTrue(comment.liked)
        self.assertIsNone(comment.type)


if __name__ == '__main__':
    unittest.main()
