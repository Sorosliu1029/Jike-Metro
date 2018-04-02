# -*- coding: utf-8 -*-

"""
Object type for topic

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

Topic = namedtuple_with_defaults(
    namedtuple('Topic',
               [
                   'briefIntro',
                   'content',
                   'createdAt',
                   'enableForUserPost',
                   'enablePictureComments',
                   'id',
                   'isAnonymous',
                   'isDreamTopic',
                   'isValid',
                   'keywords',
                   'lastMessagePostTime',
                   'likeIcon',
                   'maintainer',
                   'messagePrefix',
                   'newCategory',
                   'operateStatus',
                   'pictureUrl',
                   'rectanglePicture',
                   'ref',
                   'squarePicture',
                   'subscribedAt',
                   'subscribedStatusRawValue',
                   'subscribersCount',
                   'thumbnailUrl',
                   'timeForRank',
                   'topicId',
                   'topicType',
                   'updatedAt'
               ])
)
