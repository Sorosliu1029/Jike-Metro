# -*- coding: utf-8 -*-

"""
Base class for sequence data structure

Intended for
- Jike Collection
- Jike User Post
- Jike User Created Topic
- Jike User Subscribed Topic
- Jike User Following
- Jike User Follower
"""

from collections.abc import Iterable, Sequence


class JikeSequenceBase(Sequence):
    def __init__(self):
        super().__init__()
        self.seq = []

    def __repr__(self):
        return f'JikeSequenceBase({len(self.seq)} items)'

    def __getitem__(self, item):
        return self.seq[item]

    def __contains__(self, item):
        return any((item['content'] == ele['content'] for ele in self.seq))

    def __len__(self):
        return len(self.seq)

    def __reversed__(self):
        return reversed(self.seq)

    def index(self, value, start=0, stop=None):
        pass

    def append(self, item):
        self.seq.append(item)

    def clear(self):
        self.seq.clear()

    def extend(self, items):
        assert isinstance(items, Iterable)
        self.seq.extend(list(items))
