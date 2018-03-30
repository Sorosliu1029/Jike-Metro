# -*- coding: utf-8 -*-

"""
Object type for following update
"""

from .JikeSpecial import JikeStreamBase, JikeFetcher
from ..constants import ENDPOINTS
from ..utils import converter


class FollowingUpdate(JikeStreamBase, JikeFetcher):
    def __init__(self, jike_session, maxlen=200):
        super().__init__(maxlen)
        JikeFetcher.__init__(self, jike_session)

    def __repr__(self):
        return f'FollowingUpdate({len(self.queue)})'

    def load_more(self):
        payload = {
            'trigger': 'user',
            'loadMoreKey': self.load_more_key
        }
        result = super().fetch_more(ENDPOINTS['following_update'], payload)
        self.load_more_key = result['loadMoreKey']
        more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more
