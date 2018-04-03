# -*- coding: utf-8 -*-

"""
This module provides constants for Jike.
"""

import re
import os
from string import Template

JIKE_URI_SCHEME_FMT = 'jike://page.jk/web?url=https%3A%2F%2Fruguoapp.com%2Faccount%2Fscan%3Fuuid%3D{uuid}&displayHeader=false&displayFooter=false'

AUTH_TOKEN_STORE_PATH = os.path.join(os.path.expanduser('~'), '.local', 'jike', 'jike_metro.json')
if not os.path.exists(os.path.dirname(AUTH_TOKEN_STORE_PATH)):
    os.makedirs(os.path.dirname(AUTH_TOKEN_STORE_PATH))

STREAM_CAPACITY_LIMIT = 1000

CHECK_UNREAD_COUNT_PERIOD = 60 * 3

URL_VALIDATION_PATTERN = re.compile(
    r'(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:[/?]\S*)', re.IGNORECASE)

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
        <div class="footer_line"><strong>Code Reviews</strong>, <strong>Feedbacks</strong> and <strong>Contributions</strong> are warmly welcome.</div>
        <div class="footer_line">
            <a href="https://github.com/Sorosliu1029/Jike-Metro/issues/new" target="_blank">Open an issue</a> or
            <!--TODO Fulfill href here-->
            <a href="#" target="_blank">Leave a comment</a>
        </div>
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

_f_ = {
    '_s_': 'https',
    '_d_': 'app.jike.ruguoapp.com',
    '_v_': '1.0',
    '_p_': '{t}'
}
ENDPOINTS = {
    # login
    'create_session': '{_s_}://{_d_}/sessions.create'.format(**_f_),
    'wait_login': '{_s_}://{_d_}/sessions.wait_for_login'.format(**_f_),
    'confirm_login': '{_s_}://{_d_}/sessions.wait_for_confirmation'.format(**_f_),
    # myself
    'my_collections': '{_s_}://{_d_}/{_v_}/users/collections/list'.format(**_f_),
    # main page info stream
    'news_feed': '{_s_}://{_d_}/{_v_}/newsFeed/list'.format(**_f_),
    'news_feed_unread_count': '{_s_}://{_d_}//{_v_}/newsFeed/countUnreads'.format(**_f_),
    'following_update': '{_s_}://{_d_}/{_v_}/personalUpdate/followingUpdates'.format(**_f_),
    # user
    'user_profile': '{_s_}://{_d_}/{_v_}/users/profile'.format(**_f_),
    'user_post': '{_s_}://{_d_}/{_v_}/personalUpdate/single'.format(**_f_),
    'user_created_topic': '{_s_}://{_d_}/{_v_}/customTopics/custom/listCreated'.format(**_f_),
    'user_subscribed_topic': '{_s_}://{_d_}/{_v_}/users/topics/listSubscribed'.format(**_f_),
    'user_following': '{_s_}://{_d_}/{_v_}/userRelation/getFollowingList'.format(**_f_),
    'user_follower': '{_s_}://{_d_}/{_v_}/userRelation/getFollowerList'.format(**_f_),
    # topic
    'topic_selected': '{_s_}://{_d_}/{_v_}/messages/history'.format(**_f_),
    'topic_square': '{_s_}://{_d_}/{_v_}/squarePosts/list'.format(**_f_),
    # comment
    'list_comment': '{_s_}://{_d_}/{_v_}/comments/listPrimary'.format(**_f_),
    # creation
    'create_post': '{_s_}://{_d_}/{_v_}/originalPosts/create'.format(**_f_),
    'delete_post': '{_s_}://{_d_}/{_v_}/originalPosts/remove'.format(**_f_),
    'extract_link': '{_s_}://{_d_}/{_v_}/readability/extract'.format(**_f_),
    'picture_uptoken': 'https://upload.jike.ruguoapp.com/token',
    'picture_upload': 'https://up.qbox.me/',
    # interaction
    'like_it': '{_s_}://{_d_}/{_v_}/{_p_}/like'.format(**_f_),
    'unlike_it': '{_s_}://{_d_}/{_v_}/{_p_}/unlike'.format(**_f_),
    'collect_it': '{_s_}://{_d_}/{_v_}/{_p_}/collect'.format(**_f_),
    'uncollect_it': '{_s_}://{_d_}/{_v_}/{_p_}/uncollect'.format(**_f_),
    'repost_it': '{_s_}://{_d_}/{_v_}/reposts/add'.format(**_f_),
    'comment_it': '{_s_}://{_d_}/{_v_}/comments/add'.format(**_f_),
    # search
    'search_topic': '{_s_}://{_d_}/{_v_}/users/topics/search'.format(**_f_),
}
