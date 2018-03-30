# -*- coding: utf-8 -*-

"""
Client that Jikers play with
"""

from .session import JikeSession
from .objects import Collection, Myself, NewsFeed, FollowingUpdate
from .utils import read_token, write_token, login


class JikeClient:
    def __init__(self):
        self.auth_token = read_token()
        if self.auth_token is None:
            self.auth_token = login()
            write_token(self.auth_token)
        self.jike_session = JikeSession(self.auth_token)

        self.collection = None
        self.myself = None
        self.news_feed = None
        self.following_update = None

    def get_my_collection(self):
        if self.collection is None:
            self.collection = Collection(self.jike_session)
            self.collection.load_more()
        return self.collection

    def get_my_profile(self):
        if self.myself is None:
            self.myself = Myself(self.jike_session)
        return self.myself

    def get_news_feed(self):
        if self.news_feed is None:
            self.news_feed = NewsFeed(self.jike_session)
            self.news_feed.load_more()
        return self.news_feed

    def get_news_feed_unread_count(self):
        if self.news_feed is None:
            self.news_feed = NewsFeed(self.jike_session)
            self.news_feed.load_more()
        return self.news_feed.get_unread_count()

    def get_following_update(self):
        if self.following_update is None:
            self.following_update = FollowingUpdate(self.jike_session)
            self.following_update.load_more()
        return self.following_update

    def get_user_post(self, username):
        pass

    def get_user_created_topic(self, username):
        pass

    def get_user_subscribed_topic(self, username):
        pass

    def get_user_following(self, username):
        pass

    def get_user_follower(self, username):
        pass

    def get_comment(self, target_id):
        pass
