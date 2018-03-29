# -*- coding: utf-8 -*-

"""
This module provides constants for Jike.
"""

from string import Template
import os.path as osp

JIKE_URI_SCHEME_FMT = 'jike://page.jk/web?url=https%3A%2F%2Fruguoapp.com%2Faccount%2Fscan%3Fuuid%3D{uuid}&displayHeader=false&displayFooter=false'

AUTH_TOKEN_STORE_PATH = osp.join(osp.dirname(__file__), 'persistence', 'metro.json')

RENDER2BROWSER_HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Jike Metro</title>
    <style type="text/css">
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-around;
        }

        .header {
            font-size: 40px;
            margin: 50px auto;
        }

        .footer {
            font-size: 16px;
            margin: 100px auto;
        }

        .footer_line {
            margin: 10px auto;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">Scan for Ⓙ 🚇 🎟️</div>
    ${qrcode_svg}
    <div class="footer container">
        <div class="footer_line">🚧 with 🐈 by 👷 <a href="https://web.okjike.com/user/WalleMax/" target="_blank">挖地道的</a></div>
        <div class="footer_line">GitHub: <a href="https://github.com/Sorosliu1029/Jike-Metro" target="_blank">Jike Metro</a></div>
        <div class="footer_line"><strong>Reviews</strong>, <strong>Feedbacks</strong> and <strong>Contributions</strong> are warmly welcome.</div>
    </div>
</div>
</body>
</html>
""")

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
