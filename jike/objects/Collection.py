# -*- coding: utf-8 -*-

"""
Object type for collection
"""

from .JikeSequenceBase import JikeSequenceBase
from ..constants import ENDPOINTS
from ..utils import converter


class Collection(JikeSequenceBase):
    def __init__(self, jike_session):
        super().__init__()
        self.jike_session = jike_session
        self.load_more_key = None

    def __repr__(self):
        return f'Collection({len(self.seq)} items)'

    def index(self, value, start=0, stop=None):
        assert hasattr(value, 'name')
        for idx, item in enumerate(self.seq):
            if item['name'] == value['name']:
                return idx
        else:
            return -1

    def fetch_more(self, limit=20):
        payload = {
            'limit': limit,
            'loadMoreKey': self.load_more_key,
        }
        res = self.jike_session.post(ENDPOINTS['my_collections'], json=payload)
        if res.ok:
            result = res.json()
        res.raise_for_status()
        self.load_more_key = result['loadMoreKey']
        more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more
