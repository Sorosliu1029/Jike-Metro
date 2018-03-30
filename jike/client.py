# -*- coding: utf-8 -*-

"""
Client that Jikers play with
"""

from .session import JikeSession
from .objects import List, Stream, Myself, User, Topic
from .utils import read_token, write_token, login
from .constants import ENDPOINTS


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
            self.collection = List(self.jike_session, ENDPOINTS['my_collections'])
            self.collection.load_more()
        return self.collection

    def get_my_profile(self):
        if self.myself is None:
            self.myself = Myself(self.jike_session)
        return self.myself

    def get_news_feed(self):
        if self.news_feed is None:
            self.news_feed = Stream(self.jike_session, ENDPOINTS['news_feed'])
            self.news_feed.load_more()
        return self.news_feed

    def get_news_feed_unread_count(self):
        res = self.jike_session.get(ENDPOINTS['news_feed_unread_count'])
        if res.ok:
            result = res.json()
            return result['newMessageCount']
        res.raise_for_status()

    def get_following_update(self):
        if self.following_update is None:
            self.following_update = Stream(self.jike_session, ENDPOINTS['following_update'])
            self.following_update.load_more()
        return self.following_update

    def get_user_profile(self, username):
        res = self.jike_session.get(ENDPOINTS['user_profile'], {
            'username': username
        })
        if res.ok:
            result = res.json()
            result['user'].update(result['statsCount'])
            return User(**result['user'])
        res.raise_for_status()

    def get_user_post(self, username, limit=20):
        posts = List(self.jike_session, ENDPOINTS['user_post'], {'username': username})
        posts.load_more(limit)
        return posts

    def get_user_created_topic(self, username, limit=20):
        created_topics = List(self.jike_session, ENDPOINTS['user_created_topic'], {'username': username}, Topic)
        created_topics.load_more(limit)
        return created_topics

    def get_user_subscribed_topic(self, username, limit=20):
        subscribed_topics = List(self.jike_session, ENDPOINTS['user_subscribed_topic'], {'username': username}, Topic)
        subscribed_topics.load_more(limit)
        return subscribed_topics

    def get_user_following(self, username, limit=20):
        user_followings = List(self.jike_session, ENDPOINTS['user_following'], {'username': username}, User)
        user_followings.load_more(limit)
        return user_followings

    def get_user_follower(self, username, limit=20):
        user_followers = List(self.jike_session, ENDPOINTS['user_follower'], {'username': username}, User)
        user_followers.load_more(limit)
        return user_followers

    def get_comment(self, target_id, target_type):
        comments = Stream(self.jike_session, ENDPOINTS['comment'], {
            'targetId': target_id,
            'targetType': target_type
        })
        comments.load_more()
        return comments

    def get_topic_selected(self, topic_id):
        topic_selected = Stream(self.jike_session, ENDPOINTS['topic_selected'], {
            'topic': topic_id
        })
        topic_selected.load_more()
        return topic_selected

    def get_topic_square(self, topic_id):
        topic_square = Stream(self.jike_session, ENDPOINTS['topic_square'], {
            'topicId': topic_id
        })
        topic_square.load_more()
        return topic_square
