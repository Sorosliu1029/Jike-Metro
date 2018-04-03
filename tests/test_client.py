import unittest
import requests
from unittest.mock import *

from jike.client import JikeClient


class TestJikeClient(unittest.TestCase):
    def setUp(self):
        self.read_token = patch('jike.client.read_token').start()
        self.timer_start = patch('jike.client.Timer.start').start()

        self.MockJikeSession = patch('jike.client.JikeSession').start()
        self.mock_jike_session = Mock()
        self.MockJikeSession.return_value = self.mock_jike_session

        self.MockList = patch('jike.client.List').start()
        self.MockStream = patch('jike.client.Stream').start()

        self.MockUser = patch('jike.client.User').start()
        self.mock_user = Mock()
        self.MockUser.return_value = self.mock_user

        self.read_token.return_value = 'token'
        self.timer_start.return_value = None
        self.jike_client = JikeClient(sync_unread=True)

    def tearDown(self):
        del self.jike_client.jike_session
        patch.stopall()

    def test_init(self):
        self.assertEqual(self.jike_client.auth_token, 'token')
        self.assertIsNotNone(self.jike_client.jike_session)
        self.assertIsNone(self.jike_client.collection)
        self.assertIsNone(self.jike_client.news_feed)
        self.assertIsNone(self.jike_client.following_update)
        self.assertEqual(self.jike_client.unread_count, 0)
        self.read_token.assert_called_once()
        self.MockJikeSession.assert_called_once()
        self.timer_start.assert_called_once()
        # first login
        self.read_token.return_value = None
        with patch('jike.client.login', return_value='login_token') as login, \
                patch('jike.client.write_token', return_value=None) as token_write:
            JikeClient()
            login.assert_called_once()
            token_write.assert_called_once()

    @patch.object(JikeClient, 'get_user_profile')
    def test_get_my_profile(self, mock_get_user_profile):
        profile = {'user': 'jike'}
        mock_get_user_profile.return_value = profile
        result = self.jike_client.get_my_profile()
        self.assertEqual(result, profile)
        mock_get_user_profile.assert_called_once_with(username=None)

    def test_get_my_collection(self):
        mock_collection = Mock()
        self.MockList.return_value = mock_collection
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_my_collection()
        self.assertEqual(result, mock_collection)
        self.assertEqual(self.jike_client.collection, mock_collection)
        self.MockList.assert_called_once()
        mock_collection.load_more.assert_called_once()
        # second call
        self.MockList.reset_mock()
        result = self.jike_client.get_my_collection()
        self.assertEqual(result, mock_collection)
        self.MockList.assert_not_called()

    def test_get_news_feed_unread_count(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'newMessageCount': 0}
        self.mock_jike_session.get.return_value = mock_response
        result = self.jike_client.get_news_feed_unread_count()
        self.assertEqual(result, 0)
        self.assertEqual(self.jike_client.unread_count, 0)
        # failed call
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.get_news_feed_unread_count()

    def test_get_news_feed(self):
        mock_news_feed = Mock()
        self.MockStream.return_value = mock_news_feed
        self.MockStream.load_more.return_value = None
        result = self.jike_client.get_news_feed()
        self.assertEqual(result, mock_news_feed)
        self.assertEqual(self.jike_client.news_feed, mock_news_feed)
        self.MockStream.assert_called_once()
        mock_news_feed.load_more.assert_called_once()
        # second call
        self.MockStream.reset_mock()
        result = self.jike_client.get_news_feed()
        self.assertEqual(result, mock_news_feed)
        self.MockStream.assert_not_called()

    def test_get_following_update(self):
        mock_following_update = Mock()
        self.MockStream.return_value = mock_following_update
        self.MockStream.load_more.return_value = None
        result = self.jike_client.get_following_update()
        self.assertEqual(result, mock_following_update)
        self.assertEqual(self.jike_client.following_update, mock_following_update)
        self.MockStream.assert_called_once()
        mock_following_update.load_more.assert_called_once()
        # second call
        self.MockStream.reset_mock()
        result = self.jike_client.get_following_update()
        self.assertEqual(result, mock_following_update)
        self.MockStream.assert_not_called()

    def test_get_user_profile(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'user': {'name': 'jike'}, 'statsCount': {'count': 1}}
        self.mock_jike_session.get.return_value = mock_response
        result = self.jike_client.get_user_profile('jike')
        self.assertEqual(result, self.mock_user)
        # failed call
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.get_user_profile('jike')

    def test_get_user_post(self):
        mock_posts = Mock()
        self.MockList.return_value = mock_posts
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_user_post('jike')
        self.assertEqual(result, mock_posts)
        self.MockList.assert_called_once()
        mock_posts.load_more.assert_called_once()

    def test_get_user_created_topic(self):
        mock_topics = Mock()
        self.MockList.return_value = mock_topics
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_user_created_topic('jike')
        self.assertEqual(result, mock_topics)
        self.MockList.assert_called_once()
        mock_topics.load_more.assert_called_once()

    def test_get_user_subscribed_topic(self):
        mock_topics = Mock()
        self.MockList.return_value = mock_topics
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_user_subscribed_topic('jike')
        self.assertEqual(result, mock_topics)
        self.MockList.assert_called_once()
        mock_topics.load_more.assert_called_once()

    def test_get_user_following(self):
        mock_users = Mock()
        self.MockList.return_value = mock_users
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_user_following('jike')
        self.assertEqual(result, mock_users)
        self.MockList.assert_called_once()
        mock_users.load_more.assert_called_once()

    def test_get_user_follower(self):
        mock_users = Mock()
        self.MockList.return_value = mock_users
        self.MockList.load_more.return_value = None
        result = self.jike_client.get_user_follower('jike')
        self.assertEqual(result, mock_users)
        self.MockList.assert_called_once()
        mock_users.load_more.assert_called_once()

    def test_get_comment(self):
        mock_message = Mock()
        mock_message.type = 'OFFICIAL_MESSAGE'
        mock_message.id = '123'

        mock_comments = Mock()
        self.MockStream.return_value = mock_comments
        self.MockStream.load_more.return_value = None
        result = self.jike_client.get_comment(mock_message)
        self.assertEqual(result, mock_comments)
        self.MockStream.assert_called_once()
        mock_comments.load_more.assert_called_once()

    def test_get_topic_selected(self):
        mock_posts = Mock()
        self.MockStream.return_value = mock_posts
        self.MockStream.load_more.return_value = None
        result = self.jike_client.get_topic_selected('123')
        self.assertEqual(result, mock_posts)
        self.MockStream.assert_called_once()
        mock_posts.load_more.assert_called_once()

    def test_get_topic_square(self):
        mock_posts = Mock()
        self.MockStream.return_value = mock_posts
        self.MockStream.load_more.return_value = None
        result = self.jike_client.get_topic_square('123')
        self.assertEqual(result, mock_posts)
        self.MockStream.assert_called_once()
        mock_posts.load_more.assert_called_once()

    def test_open_in_browser(self):
        ojbk = 'https://ojbk.com/'
        # open url
        with patch('webbrowser.open') as cm:
            self.jike_client.open_in_browser(ojbk)
        cm.assert_called_once_with(ojbk)
        # open message of `namedtuple`
        message_namedtuple = Mock()
        message_namedtuple.linkInfo = {'linkUrl': ojbk}
        with patch('webbrowser.open') as cm:
            self.jike_client.open_in_browser(message_namedtuple)
        cm.assert_called_once_with(ojbk)
        # open message of `dict`
        with patch('webbrowser.open') as cm:
            self.jike_client.open_in_browser({'linkInfo': {'linkUrl': ojbk}})
        cm.assert_called_once_with(ojbk)
        # open message with 'content', which has urls in it
        urls = ['a', ojbk]
        message_namedtuple.content = 'abc'
        with patch('jike.client.extract_url', return_value=urls), \
             patch('webbrowser.open') as cm:
            self.jike_client.open_in_browser(message_namedtuple)
        cm.assert_called_with(ojbk)
        # not a url
        with self.assertRaises(ValueError):
            self.jike_client.open_in_browser([])
        # not a valid url
        with self.assertRaises(ValueError):
            self.jike_client.open_in_browser('123')

    def test_create_my_post(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'data': {}}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client.create_my_post('jike')
        self.assertIsInstance(result, tuple)
        # failed by post no string content
        with self.assertRaises(AssertionError):
            self.jike_client.create_my_post(123)
        # failed call by post both link and picture at one time
        with self.assertRaises(ValueError):
            self.jike_client.create_my_post('jike', link='a', pictures='b')
        mock_response.reset_mock()
        # failed call by post failed
        mock_response.json.return_value = {'success': False}
        with self.assertRaises(RuntimeError):
            self.jike_client.create_my_post('jike')
        # failed call by server error
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.create_my_post('jike')

    def test_delete_my_post(self):
        mock_message = Mock()
        mock_message.type = 'ORIGINAL_POST'
        mock_message.id = '123'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client.delete_my_post(mock_message)
        self.assertTrue(result)
        # failed call by no post id provided
        with self.assertRaises(AssertionError):
            self.jike_client.delete_my_post(None)
        # failed call by server error
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.delete_my_post(mock_message)

    def test__like_action(self):
        mock_message = Mock()
        mock_message.type = 'OFFICIAL_MESSAGE'
        mock_message.id = '123'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client._like_action(mock_message, 'like_it')
        self.assertTrue(result)
        # failed call by assertion
        mock_message.type = ''
        with self.assertRaises(AssertionError):
            self.jike_client._like_action(mock_message, 'unlike_it')
        # failed by server error
        mock_message.type = 'ORIGINAL_POST'
        mock_response.status_code = 402
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client._like_action(mock_message, 'like_it')

    def test_like_it(self):
        with patch('jike.client.JikeClient._like_action', return_value=None) as cm:
            client = JikeClient()
            client.like_it('msg')
        cm.assert_called_once_with('msg', 'like_it')

    def test_unlike_it(self):
        with patch('jike.client.JikeClient._like_action', return_value=None) as cm:
            client = JikeClient()
            client.unlike_it('msg')
        cm.assert_called_once_with('msg', 'unlike_it')

    def test__collect_action(self):
        mock_message = Mock()
        mock_message.type = 'OFFICIAL_MESSAGE'
        mock_message.id = '123'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client._collect_action(mock_message, 'collect_it')
        self.assertTrue(result)
        # failed call by assertion
        mock_message.type = ''
        with self.assertRaises(AssertionError):
            self.jike_client._collect_action(mock_message, 'uncollect_it')
        # failed by server error
        mock_message.type = 'ORIGINAL_POST'
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client._collect_action(mock_message, 'collect_it')

    def test_collect_it(self):
        with patch('jike.client.JikeClient._collect_action', return_value=None) as cm:
            client = JikeClient()
            client.collect_it('msg')
        cm.assert_called_once_with('msg', 'collect_it')

    def test_uncollect_it(self):
        with patch('jike.client.JikeClient._collect_action', return_value=None) as cm:
            client = JikeClient()
            client.uncollect_it('msg')
        cm.assert_called_once_with('msg', 'uncollect_it')

    def test_repost_it(self):
        mock_message = Mock()
        mock_message.type = 'OFFICIAL_MESSAGE'
        mock_message.id = '123'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'data': {}}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client.repost_it('jike', mock_message)
        self.assertIsInstance(result, tuple)
        # failed by post no string content
        with self.assertRaises(AssertionError):
            self.jike_client.repost_it(123, mock_message)
        # failed call by assertion
        mock_message.type = ''
        with self.assertRaises(AssertionError):
            self.jike_client.repost_it('jike', mock_message)
        # failed call by post failed
        mock_message.type = 'ORIGINAL_POST'
        mock_response.json.return_value = {'success': False}
        with self.assertRaises(RuntimeError):
            self.jike_client.repost_it('jike', mock_message)
        # failed by server error
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.repost_it('jike', mock_message)

    def test_comment_it(self):
        mock_message = Mock()
        mock_message.type = 'OFFICIAL_MESSAGE'
        mock_message.id = '123'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'data': {}}
        mock_response.raise_for_status.return_value = None
        self.mock_jike_session.post.return_value = mock_response
        result = self.jike_client.comment_it('jike', mock_message)
        self.assertIsInstance(result, tuple)
        # failed by post no string content
        with self.assertRaises(AssertionError):
            self.jike_client.comment_it(123, mock_message)
        # failed call by assertion
        mock_message.type = ''
        with self.assertRaises(AssertionError):
            self.jike_client.comment_it('jike', mock_message)
        # failed call by post failed
        mock_message.type = 'ORIGINAL_POST'
        mock_response.json.return_value = {'success': False}
        with self.assertRaises(RuntimeError):
            self.jike_client.comment_it('jike', mock_message)
        # failed by server error
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(requests.HTTPError):
            self.jike_client.comment_it('jike', mock_message)

    def test_search_topic(self):
        mock_topics = Mock()
        self.MockList.return_value = mock_topics
        self.MockList.load_more.return_value = None
        result = self.jike_client.search_topic('jike')
        self.assertEqual(result, mock_topics)
        self.MockList.assert_called_once()
        mock_topics.load_more.assert_called_once()

    def test__create_new_jike_session(self):
        self.jike_client.auth_token = 'new_token'
        self.jike_client._create_new_jike_session()
        self.MockJikeSession.assert_called_with('new_token')


if __name__ == '__main__':
    unittest.main()
