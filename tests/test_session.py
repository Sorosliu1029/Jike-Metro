import unittest
import requests
import responses
from urllib.parse import urlencode

from jike.session import JikeSession


class TestJikeSession(unittest.TestCase):
    def setUp(self):
        self.jike_session = JikeSession('token')

    def tearDown(self):
        del self.jike_session

    def test_init(self):
        self.assertIsInstance(self.jike_session.session, requests.Session)
        self.assertEqual(self.jike_session.token, 'token')
        self.assertEqual(self.jike_session.headers['x-jike-app-auth-jwt'], 'token')

    def test_repr(self):
        self.assertEqual(repr(self.jike_session), 'JikeSession(token...token)')

    @responses.activate
    def test_get(self):
        url = 'https://test/'
        params = {'a': 'b'}
        responses.add(responses.GET, url, status=200)
        self.jike_session.get(url, params=params)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, url + '?' + urlencode(params))
        self.assertEqual(responses.calls[0].request.headers['x-jike-app-auth-jwt'], 'token')
        self.assertEqual(responses.calls[0].response.status_code, 200)

    @responses.activate
    def test_post(self):
        url = 'https://test/'
        params = {'a': 'b'}
        json = {'x': 'y'}
        responses.add(responses.POST, url, json=json, status=200)
        self.jike_session.post(url, params=params, json=json)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, url + '?' + urlencode(params))
        self.assertEqual(responses.calls[0].request.headers['x-jike-app-auth-jwt'], 'token')
        self.assertEqual(responses.calls[0].response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
