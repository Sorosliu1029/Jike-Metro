# -*- coding: utf-8 -*-

"""
Base class for stream data structure

Intended for
- Jike News Feed
- Jike Following Update
"""

from collections import deque
from collections.abc import Iterable


class JikeStreamBase:
    def __init__(self, maxlen=200):
        self.queue = deque(maxlen=maxlen)

    def __repr__(self):
        return f'JikeStreamBase({len(self.queue)} items)'

    def __contains__(self, item):
        return any((item['id'] == ele['id'] for ele in self.queue))

    def __len__(self):
        return len(self.queue)

    def __reversed__(self):
        return reversed(self.queue)

    def index(self, value, start=0, stop=None):
        assert hasattr(value, 'id')
        for idx, item in enumerate(self.queue[start:stop]):
            if item['id'] == value['id']:
                return idx
        else:
            raise ValueError(f'Value with id: {value["id"]} not found')

    def append(self, item):
        self.queue.append(item)

    def clear(self):
        self.queue.clear()

    def extend(self, items):
        assert isinstance(items, Iterable)
        self.queue.extend(items)

    def popleft(self):
        self.queue.popleft()
