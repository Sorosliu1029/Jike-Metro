# -*- coding: utf-8 -*-

"""
Object type for type: 'OFFICIAL_MESSAGE'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

OfficialMessage = namedtuple_with_defaults(
    namedtuple('OfficialMessage',
               [
                   'abstract',
                   'collected',
                   'collectedTime',
                   'commentCount',
                   'content',
                   'createdAt',
                   'id',
                   'isCommentForbidden',
                   'likeCount',
                   'liked',
                   'linkInfo',
                   'pictures',
                   'video',
                   'repostCount',
                   'status',
                   'topic',
                   'type',
               ])
)
