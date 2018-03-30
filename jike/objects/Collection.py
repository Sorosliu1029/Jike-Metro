# -*- coding: utf-8 -*-

"""
Object type for collection
"""

from .JikeSpecial import JikeSequenceBase, JikeFetcher
from ..constants import ENDPOINTS
from ..utils import converter


class Collection(JikeSequenceBase, JikeFetcher):
    def __init__(self, jike_session):
        super().__init__()
        JikeFetcher.__init__(self, jike_session)

    def __repr__(self):
        return f'Collection({len(self.seq)} items)'

    def load_more(self, limit=20):
        payload = {
            'limit': limit,
            'loadMoreKey': self.load_more_key,
        }
        result = super().fetch_more(ENDPOINTS['my_collections'], payload)
        self.load_more_key = result['loadMoreKey']
        more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more
