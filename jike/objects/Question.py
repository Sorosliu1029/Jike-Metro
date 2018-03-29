# -*- coding: utf-8 -*-

"""
Object type for type: 'QUESTION'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

Question = namedtuple_with_defaults(
    namedtuple('Question',
               [
                   'answerCount',
                   'collected',
                   'content',
                   'createdAt',
                   'id',
                   'likeCount',
                   'likeIcon',
                   'liked',
                   'pictures',
                   'read',
                   'repostCount',
                   'status',
                   'title',
                   'topic',
                   'type',
                   'updatedAt',
                   'user',
                   'viewType'
               ])
)
