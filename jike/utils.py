# -*- coding: utf-8 -*-

"""
utils
"""

import requests
import json
import os
from collections import defaultdict
from mimetypes import guess_type

from .qr_code import make_qrcode
from .constants import ENDPOINTS, AUTH_TOKEN_STORE_PATH, URL_VALIDATION_PATTERN
from .objects.message import *

converter = defaultdict(lambda: dict,
                        {
                            'OFFICIAL_MESSAGE': OfficialMessage,
                            'ORIGINAL_POST': OriginalPost,
                            'QUESTION': Question,
                            'ANSWER': Answer,
                            'REPOST': Repost,
                            'PERSONAL_UPDATE': PersonalUpdate,
                            'PERSONAL_UPDATE_SECTION': PersonalUpdateSection,
                            'COMMENT': Comment,
                        })


def read_token():
    if os.path.exists(AUTH_TOKEN_STORE_PATH):
        with open(AUTH_TOKEN_STORE_PATH, 'rt', encoding='utf-8') as fp:
            store = json.load(fp)
        return store['auth_token']


def write_token(token):
    with open(AUTH_TOKEN_STORE_PATH, 'wt', encoding='utf-8') as fp:
        store = {
            'auth_token': token
        }
        json.dump(store, fp, indent=2)


def wait_login(uuid):
    res = requests.get(ENDPOINTS['wait_login'], params=uuid)
    if res.status_code == 200:
        logged_in = res.json()
        return logged_in['logged_in']
    res.raise_for_status()
    return False


def confirm_login(uuid):
    res = requests.get(ENDPOINTS['confirm_login'], params=uuid)
    if res.status_code == 200:
        confirmed = res.json()
        if confirmed['confirmed'] is True:
            return confirmed['token']
        else:
            raise SystemExit('User not board Jike Metro, what a shame')
    res.raise_for_status()


def login():
    res = requests.get(ENDPOINTS['create_session'])
    uuid = None
    if res.status_code == 200:
        uuid = res.json()
    res.raise_for_status()

    assert uuid, 'Create session fail'
    make_qrcode(uuid)

    logging = False
    attempt_counter = 1
    while not logging:
        logging = wait_login(uuid)
        attempt_counter += 1
        if attempt_counter > 5:
            raise SystemExit('Login takes too long, abort')

    token = None
    attempt_counter = 1
    while token is None:
        token = confirm_login(uuid)
        attempt_counter += 1
        if attempt_counter > 5:
            raise SystemExit('Login takes too long, abort')

    return token


def extract_url(content):
    return URL_VALIDATION_PATTERN.findall(content)


def extract_link(jike_session, link):
    res = jike_session.post(ENDPOINTS['extract_link'], json={
        'link': link
    })
    link_info = None
    if res.status_code == 200:
        result = res.json()
        if result['success']:
            link_info = result['data']
    res.raise_for_status()
    return link_info


def get_uptoken():
    res = requests.get(ENDPOINTS['picture_uptoken'], params={'bucket': 'jike'})
    if res.ok:
        return res.json()['uptoken']
    res.raise_for_status()


def upload_a_picture(picture):
    assert os.path.exists(picture)
    name = os.path.split(picture)[1]
    mimetype, _ = guess_type(name)
    assert mimetype
    if not mimetype.startswith('image'):
        raise ValueError('Cannot upload file: {}, which is not picture'.format(name))

    uptoken = get_uptoken()
    with open(picture, 'rb') as fp:
        files = {'token': (None, uptoken), 'file': (name, fp, mimetype)}
        res = requests.post(ENDPOINTS['picture_upload'], files=files)
    if res.status_code == 200:
        result = res.json()
        if result['success']:
            return result['key']
        else:
            raise RuntimeError('Picture upload fail')
    res.raise_for_status()


def upload_pictures(picture_paths):
    if isinstance(picture_paths, str):
        picture_paths = [picture_paths]
    pic_url = [upload_a_picture(picture) for picture in picture_paths]
    return pic_url
