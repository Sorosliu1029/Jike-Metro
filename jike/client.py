# -*- coding: utf-8 -*-

"""
Client that Jikers play with
"""

import requests
import json
from .session import JikeSession
from .qr_code import make_qrcode
from .constants import ENDPOINTS
from .objects import Collection
from .utils import converter
from .constants import AUTH_TOKEN_STORE_PATH


def read_token():
    with open(AUTH_TOKEN_STORE_PATH, 'rt', encoding='utf-8') as fp:
        store = json.load(fp)
    return store['auth_token']


def write_token(token):
    with open(AUTH_TOKEN_STORE_PATH, 'w+t', encoding='utf-8') as fp:
        store = {
            'auth_token': token
        }
        json.dump(store, fp, indent=2)


class JikeClient:
    def __init__(self):
        self.auth_token = read_token()
        if self.auth_token is None:
            self.auth_token = self.login()
            write_token(self.auth_token)
        self.jike_session = JikeSession(self.auth_token)
        self.load_more_key = {
            'my_collection': None,
        }

    @staticmethod
    def login():
        def wait_login():
            res = requests.get(ENDPOINTS['wait_login'], params=uuid)
            if res.status_code == 200:
                logged_in = res.json()
                return logged_in['logged_in']
            res.raise_for_status()
            return False

        def confirm_login():
            res = requests.get(ENDPOINTS['confirm_login'], params=uuid)
            if res.status_code == 200:
                confirmed = res.json()
                if confirmed['confirmed'] is True:
                    return confirmed['token']
            res.raise_for_status()

        res = requests.get(ENDPOINTS['create_session'])
        uuid = None
        if res.ok:
            try:
                uuid = res.json()
            except ValueError:
                raise ValueError(f'Cannot decode to json: {res.text}')
        res.raise_for_status()

        assert uuid
        make_qrcode(uuid)

        logging = False
        attempt_counter = 1
        while not logging:
            print(f'Attempt to login: {attempt_counter} time(s)')
            logging = wait_login()
            attempt_counter += 1

        token = None
        attempt_counter = 1
        while token is None:
            print(f'Wait for confirm login: {attempt_counter} time(s)')
            token = confirm_login()
            attempt_counter += 1

        return token

    def get_my_collection(self, limit=20):
        payload = {
            'limit': limit,
            'loadMoreKey': self.load_more_key['my_collection'],
        }
        res = self.jike_session.post(ENDPOINTS['get_my_collections'], json=payload)
        if res.ok:
            result = res.json()
            self.load_more_key['my_collection'] = result['loadMoreKey']
        res.raise_for_status()

        collection = (converter[item['type']](**item) for item in result['data'])
        return Collection(collection)
