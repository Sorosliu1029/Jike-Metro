# -*- coding: utf-8 -*-

"""
Object type for type: 'OFFICIAL_MESSAGE'

"""

from collections import namedtuple

# Use `namedtuple` for simplicity and efficiency
OfficialMessage = namedtuple('OfficialMessage',
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
                                 'repostCount',
                                 'status',
                                 'topic',
                                 'type',
                             ])
