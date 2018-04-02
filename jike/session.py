# -*- coding: utf-8 -*-

"""
Session that communicates with Jike server
"""

import requests
from .constants import HEADERS


class JikeSession:
    def __init__(self, token):
        self.session = requests.Session()
        self.token = token
        self.headers = dict(HEADERS)
        self.headers.update({'x-jike-app-auth-jwt': token})

    def __del__(self):
        self.session.close()

    def __repr__(self):
        return 'JikeSession({}...{})'.format(self.token[:10], self.token[-10:])

    def get(self, url, params=None):
        return self.session.get(url, params=params, headers=self.headers)

    def post(self, url, params=None, json=None):
        return self.session.post(url, params=params, json=json, headers=self.headers)
