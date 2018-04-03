# -*- coding: utf-8 -*-

"""
Special class designed for Jike Metro
"""

from collections import deque
from collections.abc import Iterable, Sequence
from ..utils import converter
from ..constants import STREAM_CAPACITY_LIMIT


class JikeSequenceBase(Sequence):
    """
    Base class for sequence data structure

    Has no size limit

    Intended for
    - Jike Collection
    - Jike User Post
    - Jike User Created Topic
    - Jike User Subscribed Topic
    - Jike User Following
    - Jike User Follower
    """

    def __init__(self):
        self.seq = []

    def __repr__(self):
        return 'JikeSequenceBase({} items)'.format(len(self.seq))

    def __getitem__(self, item):
        return self.seq[item]

    def __contains__(self, item):
        return any((item.id == ele.id for ele in self.seq))

    def __len__(self):
        return len(self.seq)

    def __reversed__(self):
        return reversed(self.seq)

    def index(self, item, start=0, stop=None):
        assert hasattr(item, 'id')
        for idx, ele in enumerate(self.seq[start:stop]):
            if ele.id == item.id:
                return idx
        raise ValueError('Item with id: {} not found'.format(item.id))

    def append(self, item):
        self.seq.append(item)

    def clear(self):
        self.seq.clear()

    def extend(self, items):
        assert isinstance(items, Iterable)
        self.seq.extend(list(items))


class JikeStreamBase:
    """
    Base class for stream data structure

    Has size limit specified by `maxlen`, default is 200

    Intended for
    - Jike News Feed
    - Jike Following Update
    - Jike Comment
    - Jike Topic Selected
    - Jike Topic Square
    """

    def __init__(self, maxlen=200):
        self.queue = deque(maxlen=maxlen)

    def __repr__(self):
        return 'JikeStreamBase({} items)'.format(len(self.queue))

    def __getitem__(self, item):
        return self.queue[item]

    def __contains__(self, item):
        return any((item.id == ele.id for ele in self.queue))

    def __len__(self):
        return len(self.queue)

    def __reversed__(self):
        return reversed(self.queue)

    def index(self, item, start=0, stop=None):
        assert hasattr(item, 'id')
        for idx, ele in enumerate(list(self.queue)[start:stop]):
            if ele.id == item.id:
                return idx
        raise ValueError('Item with id: {} not found'.format(item.id))

    def append(self, item):
        self.queue.append(item)

    def appendleft(self, item):
        self.queue.appendleft(item)

    def clear(self):
        self.queue.clear()

    def extend(self, items):
        assert isinstance(items, Iterable)
        self.queue.extend(items)

    def extendleft(self, items):
        assert isinstance(items, Iterable)
        self.queue.extendleft(items)

    def pop(self):
        return self.queue.pop()

    def popleft(self):
        return self.queue.popleft()


class JikeFetcher:
    """
    Used to fetch Jike content in json format
    """

    def __init__(self, jike_session):
        self.jike_session = jike_session
        self.load_more_key = None

    def __repr__(self):
        return 'JikeFetcher({})'.format(repr(self.jike_session))

    def fetch_more(self, endpoint, payload):
        res = self.jike_session.post(endpoint, json=payload)
        if res.status_code == 200:
            return res.json()
        res.raise_for_status()


class List(JikeSequenceBase, JikeFetcher):
    """
    Object type for Collections / Posts / Topics / Followings / Followers
    """

    def __init__(self, jike_session, endpoint, fixed_extra_payload=(), type_converter=None):
        super().__init__()
        JikeFetcher.__init__(self, jike_session)
        self.endpoint = endpoint
        self.fixed_extra_payload = dict(fixed_extra_payload)
        self.converter = type_converter

    def __repr__(self):
        return 'List({} items)'.format(len(self.seq))

    def load_more(self, limit=20, extra_payload=()):
        payload = {
            'limit': limit,
            'loadMoreKey': self.load_more_key,
        }
        payload.update(self.fixed_extra_payload)
        payload.update(dict(extra_payload))
        result = super().fetch_more(self.endpoint, payload)
        try:
            self.load_more_key = result['loadMoreKey']
        except KeyError:
            self.load_more_key = None
        if self.converter:
            more = [self.converter(**item) for item in result['data']]
        else:
            more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more

    def load_all(self, extra_payload=()):
        self.load_more(100, extra_payload)
        while self.load_more_key is not None:
            self.load_more(100, extra_payload)
        return len(self.seq)


class Stream(JikeStreamBase, JikeFetcher):
    """
    Object type for news feed
    """

    def __init__(self, jike_session, endpoint, fixed_extra_payload=(), maxlen=200):
        maxlen = min(maxlen, STREAM_CAPACITY_LIMIT)
        super().__init__(maxlen)
        JikeFetcher.__init__(self, jike_session)
        self.endpoint = endpoint
        self.fixed_extra_payload = dict(fixed_extra_payload)

    def __repr__(self):
        return 'Stream({} items, with {} capacity)'.format(len(self.queue), self.queue.maxlen)

    def load_more(self, limit=20, extra_payload=()):
        payload = {
            'trigger': 'user',
            'limit': limit,
            'loadMoreKey': self.load_more_key,
        }
        payload.update(self.fixed_extra_payload)
        payload.update(dict(extra_payload))
        result = super().fetch_more(self.endpoint, payload)
        try:
            self.load_more_key = result['loadMoreKey']
        except KeyError:
            self.load_more_key = None
        more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more

    def load_full(self, extra_payload=()):
        self.load_more(self.queue.maxlen - len(self.queue), extra_payload)

    def load_update(self, unread_count, extra_payload=()):
        assert isinstance(unread_count, int) and unread_count >= 0
        if unread_count == 0:
            return []
        current_latest_id = None if len(self) == 0 else self[0].id
        payload = {
            'trigger': 'user',
            'limit': unread_count,
            'loadMoreKey': None
        }
        payload.update(self.fixed_extra_payload)
        payload.update(dict(extra_payload))
        result = super().fetch_more(self.endpoint, payload)
        updates = []
        for item in result['data']:
            if item['id'] != current_latest_id:
                updates.append(converter[item['type']](**item))
            else:
                break
        self.extendleft(reversed(updates))
        return updates


class JikeEmitter(JikeFetcher):
    def __init__(self, jike_session, endpoint, fixed_extra_payload=()):
        super().__init__(jike_session)
        self.stopped = False
        self.endpoint = endpoint
        self.fixed_extra_payload = dict(fixed_extra_payload)

    def __repr__(self):
        return 'JikeEmitter({})'.format(repr(self.jike_session))

    def generate(self):
        while not self.stopped:
            payload = {
                'trigger': 'user',
                'limit': 100,
                'loadMoreKey': self.load_more_key,
            }
            payload.update(self.fixed_extra_payload)
            result = super().fetch_more(self.endpoint, payload)
            try:
                self.load_more_key = result['loadMoreKey']
            except KeyError:
                self.load_more_key = None
            if self.load_more_key is None:
                self.stopped = True

            for item in result['data']:
                yield item

    def stop(self):
        self.stopped = True
