# -*- coding: utf-8 -*-

"""
containing objects:

- OfficialMessage
- OriginalPost
- Repost
- Question
"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import PUBLIC_FIELDS

# Object type for type: 'OFFICIAL_MESSAGE'
OfficialMessage = namedtuple_with_defaults(
    namedtuple('OfficialMessage',
               list(set(PUBLIC_FIELDS + [
                   'abstract',
                   'video',
               ])))
)

# Object type for type: 'ORIGINAL_POST'
OriginalPost = namedtuple_with_defaults(
    namedtuple('OriginalPost',
               list(set(PUBLIC_FIELDS[:] + [
                   'messageId',
                   'poi',
               ])))
)

# Object type for type: 'REPOST'
Repost = namedtuple_with_defaults(
    namedtuple("Repost",
               list(set(PUBLIC_FIELDS[:] + [

               ])))
)

# Object type for type: 'QUESTION'
Question = namedtuple_with_defaults(
    namedtuple('Question',
               list(set(PUBLIC_FIELDS[:] + [
                   'answerCount',
                   'title',
                   'updatedAt',
               ])))
)

# Object type for type: 'COMMENT'
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
