# -*- coding: utf-8 -*-

import sys
from .client import JikeClient

options = sys.argv[1:]
if not {'news', 'follow'} & set(options):
    print('Jike Metro 🚇  : Please provide a notification option: "news: 消息" or "follow: 动态"')
else:
    c = JikeClient(sync_unread=True)
    if 'news' in options:
        c.get_news_feed()
        print('Jike Metro 🚇  will notify you when your subscribed topics update. 🐈  ')
    if 'follow' in options:
        c.get_following_update()
    print('Jike Metro 🚇  will notify you when your following users update. 🐈  ')
