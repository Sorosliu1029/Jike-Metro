# -*- coding: utf-8 -*-

"""
Object type for type: 'ORIGINAL_POST'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

OriginalPost = namedtuple_with_defaults(
    namedtuple('OriginalPost',
               [
                   'collectTime',
                   'collected',
                   'commentCount',
                   'content',
                   'createdAt',
                   'id',
                   'isCommentForbidden',
                   'likeCount',
                   'likeInfo',
                   'messageId',
                   'pictures',
                   'read',
                   'repostCount',
                   'status',
                   'topic',
                   'type',
                   'user',
                   'viewType',
               ])
)
