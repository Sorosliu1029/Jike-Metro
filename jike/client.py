# -*- coding: utf-8 -*-

"""
Client that Jikers play with
"""

from .session import JikeSession
from .objects import Collection, Myself
from .utils import read_token, write_token, login


class JikeClient:
    def __init__(self):
        self.auth_token = read_token()
        if self.auth_token is None:
            self.auth_token = login()
            write_token(self.auth_token)
        self.jike_session = JikeSession(self.auth_token)

    def get_my_collection(self):
        collection = Collection(self.jike_session)
        collection.fetch_more()
        return collection

    def get_my_profile(self):
        return Myself(self.jike_session)
