==================
Jike Metro 🚇
==================

.. image:: https://img.shields.io/travis/Sorosliu1029/Jike-Metro.svg
    :alt: Travis
    :target: https://travis-ci.org/Sorosliu1029/Jike-Metro

.. image:: https://img.shields.io/pypi/v/jike.svg
    :alt: PyPI
    :target: https://pypi.org/project/jike/

.. image:: https://img.shields.io/pypi/l/jike.svg
    :alt: PyPI - License
    :target: https://pypi.org/project/jike/

.. image:: https://img.shields.io/pypi/pyversions/jike.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/jike/

.. image:: https://img.shields.io/pypi/status/jike.svg
    :alt: PyPI - Status
    :target: https://pypi.org/project/jike/

.. image:: https://img.shields.io/github/contributors/Sorosliu1029/Jike-Metro.svg
    :alt: GitHub contributors
    :target: https://github.com/Sorosliu1029/Jike-Metro/graphs/contributors

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :alt: Say Thanks
    :target: https://saythanks.io/to/Sorosliu1029

.. image:: https://img.shields.io/github/stars/Sorosliu1029/Jike-Metro.svg?style=social&label=Stars
    :alt: GitHub stars
    :target: https://github.com/Sorosliu1029/Jike-Metro/

Jike Metro 🚇 是即刻镇的地铁工程，旨在提高即友的出行游览效率。

**安全提醒**：Jike Metro 🚇 目前是地下工作，非官方授权，随时可能翻车，给果果 🐈 买小鱼干可保平安。

.. image:: https://cdn.ruguoapp.com/Ftub2jUf092k6GYua0DTV8t-PMoR.jpg?imageView2/0/w/2000/h/400/q/50

图片来源: `即刻九号工友“果果”和小伙伴们 <https://web.okjike.com/topic/55d6de4660b2719eb447649a/official>`_

Jike Metro 🚇 简易乘车指南
==========================

.. code-block:: python

    >>> c = jike.JikeClient()
    >>> c.get_my_profile()
    User(id='58cf99696a34ae0015b9f5d5', screenName=挖地道的)
    >>> my_collection = c.get_my_collection()
    >>> my_collection[0]
    OfficialMessage(id='55dd572f41904d0e00fc58f8', content=即刻果果: 分享一只曾经的童星（已光速成长）)
    >>> news_feed = c.get_news_feed()
    >>> news_feed[0]
    OfficialMessage(id='5ac347a30799810017977041', content=DeepMind 发布新架构  让AI 边玩游戏边强化学习)
    >>> ceo = c.get_user_profile(username='82D23B32-CF36-4C59-AD6F-D05E3552CBF3')
    >>> ceo
    User(screenName=瓦恁)
    >>> c.create_my_post(content='Jike Metro 🚇 released!', link='https://github.com/Sorosliu1029/Jike-Metro')
    True

更详细的乘车指南请移步 👉 `Jike Metro 🚇 乘车指南 <https://www.0x2beace.me/Jike-Metro/>`_

Jike Metro 🚇 乘车体验
======================

Jike Metro 🚇 目前支持：

- 获取自己的收藏，查看自己的用户信息
- 流式获取首页消息和动态
- 获取某个用户的用户信息、发布的动态、创建的主题、关注的主题、TA关注的人和关注TA的人
- 获取某条消息/动态的评论
- 获取某个主题下的精选和广场
- 发布个人动态（可带图、带链接、带主题），删除个人动态
- 点赞、收藏、评论、转发某条消息/动态
- 在浏览器中打开某条消息的原始链接
- 根据关键词搜索主题

Jike Metro 🚇 现在支持 Python 3.4-3.6

Jike Metro 🚇 入口
==================

可通过 pip 安装 Jike Metro 🚇

.. code-block:: bash

    $ pip install jike

注意安全，小心行驶，不要影响其他即友的出行。

Jike Metro 🚇 基础设施
======================

Jike Metro 🚇 基于：

- `即刻Web版 <https://web.okjike.com>`_
- `requests <https://github.com/requests/requests>`_
- `qrcode <https://github.com/lincolnloop/python-qrcode>`_
