# -*- coding: utf-8 -*-

"""
Object type for type: 'COMMENT'
"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

Comment = namedtuple_with_defaults(
    namedtuple('Comment',
               [
                   'content',
                   'createdAt',
                   'enablePictureComments',
                   'hotReplies',
                   'id',
                   'level',
                   'likeCount',
                   'liked',
                   'pictures',
                   'replyCount',
                   'status',
                   'targetId',
                   'targetType',
                   'threadId',
                   'type',
                   'user'
               ])
)