# -*- coding: utf-8 -*-

"""
Object type for type: 'ORIGINAL_POST'

"""

from collections import namedtuple

OriginalPost = namedtuple('OriginalPost',
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

