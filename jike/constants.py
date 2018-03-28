# -*- coding: utf-8 -*-

"""
This module provides constants for Jike.
"""

JIKE_URI_SCHEME_FMT = 'jike://page.jk/web?url=https%3A%2F%2Fruguoapp.com%2Faccount%2Fscan%3Fuuid%3D{uuid}&displayHeader=false&displayFooter=false'

HEADERS = {
    'Origin': 'http://web.okjike.com',
    'Referer': 'http://web.okjike.com',
    # TODO change User-Agent to 'Jike Metro' once published
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',

    'x-jike-app-auth-jwt': None,
    'App-Version': '4.1.0',
    'DNT': '1',
    'platform': 'web',
}

ENDPOINTS = {
    'create_session': 'https://app.jike.ruguoapp.com/sessions.create',
    'wait_login': 'https://app.jike.ruguoapp.com/sessions.wait_for_login',
    'confirm_login': 'https://app.jike.ruguoapp.com/sessions.wait_for_confirmation',

    'get_my_collections': 'https://app.jike.ruguoapp.com/1.0/users/collections/list',
}