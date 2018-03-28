# -*- coding: utf-8 -*-

"""
Object type for type: 'QUESTION'

"""

from collections import namedtuple

Question = namedtuple('Question',
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
                          'respostCount',
                          'status',
                          'title',
                          'topic',
                          'type',
                          'updatedAt',
                          'user',
                          'viewType'
                      ])