# -*- coding: utf-8 -*-

"""
Object type for type: 'REPOST'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

Repost = namedtuple_with_defaults(
    namedtuple("Repost",
               [
                   'collectTime',
                   'collected',
                   'commentCount',
                   'content',
                   'createdAt',
                   'id',
                   'likeCount',
                   'liked',
                   'pictures',
                   'repostCount',
                   'status',
                   'target',
                   'targetType',
                   'type',
                   'user',
               ])
)
