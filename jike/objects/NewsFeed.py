# -*- coding: utf-8 -*-

"""
Object type for news feed
"""

from .JikeSpecial import JikeStreamBase, JikeFetcher
from ..constants import ENDPOINTS
from ..utils import converter


class NewsFeed(JikeStreamBase, JikeFetcher):
    def __init__(self, jike_session, maxlen=200):
        super().__init__(maxlen)
        JikeFetcher.__init__(self, jike_session)

    def __repr__(self):
        return f'NewsFeed({len(self.queue)})'

    def load_more(self):
        payload = {
            'trigger': 'user',
            'loadMoreKey': self.load_more_key
        }
        result = super().fetch_more(ENDPOINTS['news_feed'], payload)
        self.load_more_key = result['loadMoreKey']
        more = [converter[item['type']](**item) for item in result['data']]
        self.extend(more)
        return more

    def get_unread_count(self):
        res = self.jike_session.get(ENDPOINTS['news_feed_unread_count'])
        if res.ok:
            result = res.json()
            return result['newMessageCount']
        res.raise_for_status()
