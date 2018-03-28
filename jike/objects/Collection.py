# -*- coding: utf-8 -*-

"""
Object type for collection
"""

from collections.abc import Iterable, Sequence


class Collection(Sequence):
    def __init__(self, collection):
        super().__init__()
        assert isinstance(collection, Iterable)
        self.collection = list(collection)

    def __repr__(self):
        return f'Collection({len(self.collection)} items)'

    def __getitem__(self, pos):
        return self.collection[pos]

    def __contains__(self, ele):
        return any((ele.content == item.content for item in self.collection))

    def __len__(self):
        return len(self.collection)

    def append(self, ele):
        # TODO More strict instance check
        assert isinstance(ele, object)
        self.collection.append(ele)

    def clear(self):
        self.collection.clear()

    def extend(self, items):
        assert isinstance(items, Iterable)
        self.collection.extend(list(items))

    def index(self, value, start=0, stop=None):
        assert hasattr(value, 'name')
        for idx, item in enumerate(self.collection):
            if item.name == value.name:
                return idx
        else:
            return -1

    def insert(self, pos, ele):
        self.collection.insert(pos, ele)

    def __reversed__(self):
        return reversed(self.collection)

    def __setitem__(self, pos, ele):
        self.collection[pos] = ele
