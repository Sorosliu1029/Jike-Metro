# -*- coding: utf-8 -*-

"""
Object type for Collections / Posts / Topics / Followings / Followers
"""

from .JikeSpecial import JikeSequenceBase, JikeFetcher
from ..utils import converter


class List(JikeSequenceBase, JikeFetcher):
    def __init__(self, jike_session, endpoint, fixed_extra_payload=(), type_converter=None):
        super().__init__()
        JikeFetcher.__init__(self, jike_session)
        self.endpoint = endpoint
        self.fixed_extra_payload = dict(fixed_extra_payload)
        self.converter = type_converter

    def __repr__(self):
        return f'Collection({len(self.seq)} items)'

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
