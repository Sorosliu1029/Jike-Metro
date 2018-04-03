import unittest
import requests
from unittest.mock import *
from jike.objects.base import *


class TestJikeSequenceBase(unittest.TestCase):
    def setUp(self):
        self.mock_a = Mock()
        self.mock_a.id = 1
        self.mock_b = Mock()
        self.mock_b.id = 2

        self.sequence = JikeSequenceBase()

    def test_init(self):
        self.assertEqual(self.sequence.seq, [])

    def test_repr(self):
        self.assertEqual(repr(self.sequence), 'JikeSequenceBase(0 items)')

    def test_len(self):
        self.assertEqual(len(self.sequence), 0)

    def test_append(self):
        self.sequence.append(self.mock_a)
        self.assertEqual(len(self.sequence), 1)
        self.assertEqual(self.sequence[0], self.mock_a)

    def test_getitem(self):
        with self.assertRaises(IndexError):
            _ = self.sequence[0]
        self.sequence.append(self.mock_a)
        self.assertEqual(self.sequence[0], self.mock_a)

    def test_contains(self):
        self.assertFalse(self.mock_a in self.sequence)
        self.sequence.append(self.mock_a)
        self.assertTrue(self.mock_a in self.sequence)

    def test_extend(self):
        self.sequence.extend([self.mock_a, self.mock_b])
        self.assertEqual(len(self.sequence), 2)
        self.assertEqual(self.sequence[0], self.mock_a)
        self.assertEqual(self.sequence[-1], self.mock_b)

    def test_reversed(self):
        self.sequence.extend([self.mock_a, self.mock_b])
        self.assertEqual(list(reversed(self.sequence))[0], self.mock_b)
        self.assertEqual(list(reversed(self.sequence))[-1], self.mock_a)

    def test_index(self):
        self.sequence.append(self.mock_a)
        self.assertEqual(self.sequence.index(self.mock_a), 0)
        with self.assertRaises(ValueError):
            self.sequence.index(self.mock_b)

    def test_clear(self):
        self.sequence.append(self.mock_a)
        self.assertEqual(len(self.sequence), 1)
        self.sequence.clear()
        self.assertEqual(len(self.sequence), 0)


class TestJikeStreamBase(unittest.TestCase):
    def setUp(self):
        self.mock_a = Mock()
        self.mock_a.id = 1
        self.mock_b = Mock()
        self.mock_b.id = 2
        self.mock_c = Mock()
        self.mock_c.id = 3

        self.stream = JikeStreamBase(maxlen=2)

    def test_init(self):
        self.assertEqual(len(self.stream.queue), 0)
        self.assertEqual(self.stream.queue.maxlen, 2)

    def test_repr(self):
        self.assertEqual(repr(self.stream), 'JikeStreamBase(0 items)')

    def test_getitem(self):
        with self.assertRaises(IndexError):
            _ = self.stream[0]
        self.stream.append(self.mock_a)
        self.assertEqual(self.stream[0], self.mock_a)

    def test_contains(self):
        self.assertFalse(self.mock_a in self.stream)
        self.stream.append(self.mock_a)
        self.assertTrue(self.mock_a in self.stream)

    def test_len(self):
        self.assertEqual(len(self.stream), 0)

    def test_reversed(self):
        self.stream.extend([self.mock_a, self.mock_b])
        self.assertEqual(list(reversed(self.stream))[0], self.mock_b)
        self.assertEqual(list(reversed(self.stream))[-1], self.mock_a)

    def test_index(self):
        self.stream.append(self.mock_a)
        self.assertEqual(self.stream.index(self.mock_a), 0)
        with self.assertRaises(ValueError):
            self.stream.index(self.mock_b)

    def test_append(self):
        self.stream.append(self.mock_a)
        self.assertEqual(len(self.stream), 1)
        self.assertEqual(self.stream[0], self.mock_a)

    def test_appendleft(self):
        self.stream.append(self.mock_a)
        self.stream.appendleft(self.mock_b)
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[1], self.mock_a)
        self.assertEqual(self.stream[0], self.mock_b)

    def test_clear(self):
        self.stream.append(self.mock_a)
        self.assertEqual(len(self.stream), 1)
        self.stream.clear()
        self.assertEqual(len(self.stream), 0)

    def test_extend(self):
        self.stream.extend([self.mock_a, self.mock_b])
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0], self.mock_a)
        self.assertEqual(self.stream[-1], self.mock_b)

    def test_extendleft(self):
        self.stream.extendleft([self.mock_a, self.mock_b])
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0], self.mock_b)
        self.assertEqual(self.stream[-1], self.mock_a)

    def test_pop(self):
        self.stream.append(self.mock_a)
        popped = self.stream.pop()
        self.assertEqual(len(self.stream), 0)
        self.assertEqual(popped, self.mock_a)
        with self.assertRaises(IndexError):
            self.stream.pop()

    def test_popleft(self):
        self.stream.append(self.mock_a)
        self.stream.appendleft(self.mock_b)
        popped = self.stream.popleft()
        self.assertEqual(len(self.stream), 1)
        self.assertEqual(popped, self.mock_b)
        _ = self.stream.popleft()
        self.assertEqual(len(self.stream), 0)
        with self.assertRaises(IndexError):
            self.stream.popleft()


class TestJikeFetcher(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.fetcher = JikeFetcher(self.mock_session)

    def test_init(self):
        self.assertEqual(self.fetcher.jike_session, self.mock_session)
        self.assertIsNone(self.fetcher.load_more_key)

    def test_repr(self):
        self.assertEqual(repr(self.fetcher), 'JikeFetcher({})'.format(repr(self.mock_session)))

    def test_fetch_more(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'more': 'items'}
        mock_response.raise_for_status.return_value = None
        self.mock_session.post.return_value = mock_response
        self.assertEqual(self.fetcher.fetch_more(None, None), {'more': 'items'})
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError
        with self.assertRaises(requests.HTTPError):
            self.fetcher.fetch_more(None, None)


class TestList(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.list = List(self.mock_session, 'https://ojbk.com/', type_converter=dict)

    def test_init(self):
        self.assertEqual(self.list.endpoint, 'https://ojbk.com/')
        self.assertEqual(self.list.fixed_extra_payload, {})
        self.assertIs(self.list.converter, dict)

    def test_repr(self):
        self.assertEqual(repr(self.list), 'List(0 items)')

    def test_load_more(self):
        data = [{'id': 'b'}, {'id': 'c'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'loadMoreKey': 'a', 'data': data}
        self.mock_session.post.return_value = mock_response
        result = self.list.load_more()
        self.assertEqual(result, data)
        self.assertEqual(self.list.load_more_key, 'a')
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list[0], {'id': 'b'})
        self.mock_session.post.assert_called_once_with('https://ojbk.com/', json={
            'limit': 20,
            'loadMoreKey': None
        })
        mock_response.json.return_value = {'loadMoreKey': 'd', 'data': []}
        result = self.list.load_more(limit=10)
        self.assertEqual(result, [])
        self.assertEqual(self.list.load_more_key, 'd')
        self.assertEqual(len(self.list), 2)
        self.mock_session.post.assert_called_with('https://ojbk.com/', json={
            'limit': 10,
            'loadMoreKey': 'a'
        })

    def test_load_all(self):
        data = [{'id': 'b'}, {'id': 'c'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'loadMoreKey': 'a', 'data': data},
            {'loadMoreKey': None, 'data': data}
        ]
        self.mock_session.post.return_value = mock_response
        result = self.list.load_all()
        self.assertEqual(result, 4)
        self.assertIsNone(self.list.load_more_key)
        self.assertEqual(self.mock_session.post.call_count, 2)


class TestStream(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.stream = Stream(self.mock_session, 'https://ojbk.com/', maxlen=2)

    def test_init(self):
        self.assertEqual(self.stream.endpoint, 'https://ojbk.com/')
        self.assertEqual(self.stream.fixed_extra_payload, {})
        self.assertEqual(self.stream.queue.maxlen, 2)

    def test_repr(self):
        self.assertEqual(repr(self.stream), 'Stream(0 items, with 2 capacity)')

    def test_load_more(self):
        data1 = [{'id': 'b', 'type': 'OFFICIAL_MESSAGE'}, {'id': 'c', 'type': 'OFFICIAL_MESSAGE'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'loadMoreKey': 'a', 'data': data1}
        self.mock_session.post.return_value = mock_response
        result = self.stream.load_more()
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(self.stream.load_more_key, 'a')
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0].id, 'b')
        self.assertEqual(self.stream[-1].type, 'OFFICIAL_MESSAGE')
        self.mock_session.post.assert_called_once_with('https://ojbk.com/', json={
            'trigger': 'user',
            'limit': 20,
            'loadMoreKey': None
        })
        data2 = [{'id': 'd', 'type': 'REPOST'}, {'id': 'e', 'type': 'REPOST'}]
        mock_response.json.return_value = {'loadMoreKey': None, 'data': data2}
        result = self.stream.load_more(limit=10)
        self.assertIsInstance(result[0], tuple)
        self.assertIsNone(self.stream.load_more_key)
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0].id, 'd')
        self.assertEqual(self.stream[-1].type, 'REPOST')
        self.mock_session.post.assert_called_with('https://ojbk.com/', json={
            'trigger': 'user',
            'limit': 10,
            'loadMoreKey': 'a'
        })

    def test_load_full(self):
        data1 = [{'id': 'b', 'type': 'OFFICIAL_MESSAGE'}, {'id': 'c', 'type': 'OFFICIAL_MESSAGE'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'loadMoreKey': 'a', 'data': data1}
        self.mock_session.post.return_value = mock_response
        self.stream.append(None)
        self.stream.load_full()
        self.assertEqual(self.stream.load_more_key, 'a')
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0].id, 'b')
        self.assertEqual(self.stream[-1].type, 'OFFICIAL_MESSAGE')
        self.mock_session.post.assert_called_once_with('https://ojbk.com/', json={
            'trigger': 'user',
            'limit': 1,
            'loadMoreKey': None
        })

    def test_load_update(self):
        data1 = [{'id': 'b', 'type': 'OFFICIAL_MESSAGE'}, {'id': 'c', 'type': 'OFFICIAL_MESSAGE'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'loadMoreKey': 'a', 'data': data1}
        self.mock_session.post.return_value = mock_response
        result = self.stream.load_update(1)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(self.stream), 2)
        self.assertEqual(self.stream[0].id, 'b')
        self.assertEqual(self.stream[-1].type, 'OFFICIAL_MESSAGE')
        self.mock_session.post.assert_called_once_with('https://ojbk.com/', json={
            'trigger': 'user',
            'limit': 1,
            'loadMoreKey': None
        })
        result = self.stream.load_update(0)
        self.assertEqual(result, [])
        with self.assertRaises(AssertionError):
            self.stream.load_update('not an int')
        with self.assertRaises(AssertionError):
            self.stream.load_update(-1)


class TestJikeEmitter(unittest.TestCase):
    def setUp(self):
        self.mock_session = Mock()
        self.emitter = JikeEmitter(self.mock_session, 'https://ojbk.com/')

    def test_init(self):
        self.assertFalse(self.emitter.stopped)
        self.assertEqual(self.emitter.endpoint, 'https://ojbk.com/')
        self.assertEqual(self.emitter.fixed_extra_payload, {})

    def test_repr(self):
        self.assertEqual(repr(self.emitter), 'JikeEmitter({})'.format(repr(self.mock_session)))

    def test_generate(self):
        data1 = [{'id': 'b'}, {'id': 'c'}]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'loadMoreKey': 'a', 'data': data1},
            {'loadMoreKey': None, 'data': []}
        ]
        self.mock_session.post.return_value = mock_response
        result = list(self.emitter.generate())
        self.assertEqual(result, data1)
        self.assertTrue(self.emitter.stopped)
        self.assertIsNone(self.emitter.load_more_key)
        self.mock_session.post.assert_called_with('https://ojbk.com/', json={
            'trigger': 'user',
            'limit': 100,
            'loadMoreKey': 'a'
        })
        self.assertEqual(self.mock_session.post.call_count, 2)

    def test_stop(self):
        self.assertFalse(self.emitter.stopped)
        self.emitter.stop()
        self.assertTrue(self.emitter.stopped)


if __name__ == '__main__':
    unittest.main()
