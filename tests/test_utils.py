import unittest
import responses
import requests
from urllib.parse import urlencode
from unittest.mock import *

from jike import utils, constants


class TestJikeUtils(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def test_read_token(self):
        mocked_metro_json = '{"auth_token": "token"}'
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mocked_metro_json)):
            mock_token = utils.read_token()
        self.assertEqual(mock_token, 'token')

    def test_write_token(self):
        m = mock_open()
        with patch('builtins.open', m):
            utils.write_token('token')
        m.assert_called_once_with(constants.AUTH_TOKEN_STORE_PATH, 'wt', encoding='utf-8')
        handle = m()
        handle.write.assert_called()

    @responses.activate
    def test_extract_link(self):
        success_response = {'success': True, 'data': 'link'}
        responses.add(responses.POST, constants.ENDPOINTS['extract_link'],
                      json=success_response,
                      status=200)
        responses.add(responses.POST, constants.ENDPOINTS['extract_link'],
                      status=401)
        # success call
        result = utils.extract_link(self.session, 'https://www.ojbk.com')
        self.assertEqual(result, 'link')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, constants.ENDPOINTS['extract_link'])
        self.assertEqual(responses.calls[0].response.json(), success_response)
        # failed call
        with self.assertRaises(requests.HTTPError) as cm:
            utils.extract_link(self.session, 'https://www.ojbk.com')
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(cm.exception.response.status_code, 401)

    def test_extract_url(self):
        content = 'no url inside'
        self.assertEqual(utils.extract_url(content), [])
        content = 'one url inside: https://www.jike.ojbk.com/metro end this url'
        self.assertEqual(utils.extract_url(content), ['https://www.jike.ojbk.com/metro'])
        content = 'more urls ' + content + ' http://www.test.xyz/a/132-z/ end '
        self.assertEqual(utils.extract_url(content),
                         ['https://www.jike.ojbk.com/metro', 'http://www.test.xyz/a/132-z/'])

    @responses.activate
    def test_wait_login(self):
        success_response = {'logged_in': True}
        responses.add(responses.GET, constants.ENDPOINTS['wait_login'],
                      json=success_response, status=200)
        failed_response = {'logged_in': False}
        responses.add(responses.GET, constants.ENDPOINTS['wait_login'],
                      json=failed_response, status=200)
        responses.add(responses.GET, constants.ENDPOINTS['wait_login'],
                      status=500)
        uuid = {'uuid': '123'}
        # success call
        result = utils.wait_login(uuid)
        self.assertTrue(result)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, constants.ENDPOINTS['wait_login'] + '?' + urlencode(uuid))
        self.assertEqual(responses.calls[0].response.json(), success_response)
        # failed call
        result = utils.wait_login(uuid)
        self.assertFalse(result)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.url, constants.ENDPOINTS['wait_login'] + '?' + urlencode(uuid))
        self.assertEqual(responses.calls[1].response.json(), failed_response)
        # failed again call
        with self.assertRaises(requests.HTTPError) as cm:
            utils.wait_login(uuid)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(cm.exception.response.status_code, 500)

    @responses.activate
    def test_confirm_login(self):
        success_response = {'confirmed': True, 'token': 'token'}
        responses.add(responses.GET, constants.ENDPOINTS['confirm_login'],
                      json=success_response, status=200)
        failed_response = {'confirmed': False, 'token': 'token'}
        responses.add(responses.GET, constants.ENDPOINTS['confirm_login'],
                      json=failed_response, status=200)
        responses.add(responses.GET, constants.ENDPOINTS['confirm_login'],
                      status=502)
        uuid = {'uuid': '123'}
        # success call
        result = utils.confirm_login(uuid)
        self.assertEqual(result, 'token')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, constants.ENDPOINTS['confirm_login'] + '?' + urlencode(uuid))
        self.assertEqual(responses.calls[0].response.json(), success_response)
        # failed call
        with self.assertRaises(SystemExit):
            utils.confirm_login(uuid)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.url, constants.ENDPOINTS['confirm_login'] + '?' + urlencode(uuid))
        self.assertEqual(responses.calls[1].response.json(), failed_response)
        # failed again call
        with self.assertRaises(requests.HTTPError) as cm:
            utils.confirm_login(uuid)
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(cm.exception.response.status_code, 502)

    @responses.activate
    def test_login(self):
        uuid = {'uuid': '123'}
        responses.add(responses.GET, constants.ENDPOINTS['create_session'],
                      json=uuid, status=200)
        responses.add(responses.GET, constants.ENDPOINTS['create_session'],
                      status=400)
        responses.add(responses.GET, constants.ENDPOINTS['create_session'],
                      json=uuid, status=200)
        responses.add(responses.GET, constants.ENDPOINTS['create_session'],
                      json=uuid, status=200)
        # success call
        with patch('jike.utils.wait_login', return_value=True), \
             patch('jike.utils.confirm_login', return_value='token'), \
             patch('jike.utils.make_qrcode'):
            result = utils.login()
        self.assertEqual(result, 'token')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, constants.ENDPOINTS['create_session'])
        self.assertEqual(responses.calls[0].response.json(), uuid)
        # failed call
        with patch('jike.utils.wait_login', return_value=True), \
             patch('jike.utils.confirm_login', return_value='token'), \
             patch('jike.utils.make_qrcode'), \
             self.assertRaises(requests.HTTPError) as cm:
            utils.login()
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(cm.exception.response.status_code, 400)
        # failed call by `wait_login`
        with patch('jike.utils.wait_login', return_value=False), \
             patch('jike.utils.confirm_login', return_value='token'), \
             patch('jike.utils.make_qrcode'), \
             self.assertRaises(SystemExit):
            utils.login()
        self.assertEqual(len(responses.calls), 3)
        # failed call by `confirm_login`
        with patch('jike.utils.wait_login', return_value=True), \
             patch('jike.utils.confirm_login', return_value=None), \
             patch('jike.utils.make_qrcode'), \
             self.assertRaises(SystemExit):
            utils.login()
        self.assertEqual(len(responses.calls), 4)

    @responses.activate
    def test_get_uptoken(self):
        params = {'bucket': 'jike'}
        success_reponse = {'uptoken': 'token'}
        responses.add(responses.GET, constants.ENDPOINTS['picture_uptoken'],
                      json=success_reponse, status=200)
        responses.add(responses.GET, constants.ENDPOINTS['picture_uptoken'],
                      status=404)
        # success call
        result = utils.get_uptoken()
        self.assertEqual(result, 'token')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url,
                         constants.ENDPOINTS['picture_uptoken'] + '?' + urlencode(params))
        self.assertEqual(responses.calls[0].response.json(), success_reponse)
        # failed call
        with self.assertRaises(requests.HTTPError) as cm:
            utils.get_uptoken()
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(cm.exception.response.status_code, 404)

    @responses.activate
    def test_upload_a_picture(self):
        # picture not exists
        with patch('os.path.exists', return_value=False), \
             self.assertRaises(AssertionError):
            utils.upload_a_picture('jike.png')
        # cannot figure out mimetype
        with patch('os.path.exists', return_value=True), \
             patch('os.path.split', return_value=('a', 'b')), \
             patch('mimetypes.guess_type', return_value=(None, None)), \
             self.assertRaises(AssertionError):
            utils.upload_a_picture('jike.png')
        # not upload picture
        with patch('os.path.exists', return_value=True), \
             self.assertRaises(ValueError):
            utils.upload_a_picture('a.txt')

        success_reponse = {'success': True, 'key': 'key'}
        responses.add(responses.POST, constants.ENDPOINTS['picture_upload'],
                      json=success_reponse, status=200)
        failed_response = {'success': False}
        responses.add(responses.POST, constants.ENDPOINTS['picture_upload'],
                      json=failed_response, status=200)
        responses.add(responses.POST, constants.ENDPOINTS['picture_upload'],
                      status=401)
        # success call
        with patch('os.path.exists', return_value=True), \
             patch('jike.utils.get_uptoken', return_value='token'), \
             patch('builtins.open', mock_open(read_data='picture_content')):
            result = utils.upload_a_picture('jike.png')
        self.assertEqual(result, 'key')
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, constants.ENDPOINTS['picture_upload'])
        self.assertEqual(responses.calls[0].response.json(), success_reponse)
        self.assertTrue(responses.calls[0].request.headers['Content-Type'].startswith('multipart/form-data;'))
        self.assertTrue(b'jike.png' in responses.calls[0].request.body)
        # failed call
        with patch('os.path.exists', return_value=True), \
             patch('jike.utils.get_uptoken', return_value='token'), \
             patch('builtins.open', mock_open(read_data='picture_content')), \
             self.assertRaises(RuntimeError):
            utils.upload_a_picture('jike.png')
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].response.json(), failed_response)
        # failed again call
        with patch('os.path.exists', return_value=True), \
             patch('jike.utils.get_uptoken', return_value='token'), \
             patch('builtins.open', mock_open(read_data='picture_content')), \
             self.assertRaises(requests.HTTPError) as cm:
            utils.upload_a_picture('jike.png')
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(cm.exception.response.status_code, 401)

    def test_upload_pictures(self):
        with patch('jike.utils.upload_a_picture', return_value='a_url'):
            pic_urls = utils.upload_pictures('p.png')
        self.assertEqual(len(pic_urls), 1)
        with patch('jike.utils.upload_a_picture', return_value='a_url'):
            pic_urls = utils.upload_pictures(['p.png', 'q.png'])
        self.assertEqual(len(pic_urls), 2)


if __name__ == '__main__':
    unittest.main()
