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

PUBLIC_FIELDS = [
    # item meta info
    'id',
    'createdAt',
    'content',
    'pictures',
    'status',
    'topic',
    'linkInfo',
    'target',
    'targetType',
    'type',
    'user',
    'isCommentForbidden',
    'viewType',
    # item interaction info
    'likeCount',
    'likeIcon',
    'likeInfo',
    'commentCount',
    'repostCount',
    # item personal info
    'read',
    'liked',
    'collected',
    'collectedTime',
    'collectTime',  # seems to be Jike typo
]

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
                   'syncCommentId',
                   'replyToComment',
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

# Object type for type: 'ANSWER'
Answer = namedtuple_with_defaults(
    namedtuple('Answer',
               list(set(PUBLIC_FIELDS[:] + [
                   'question',
                   'questionId',
                   'richtextContent',
                   'upVoteCount',
                   'voteTend',
               ])))
)

# Object type for type: 'PERSONAL_UPDATE_SECTION'
PersonalUpdateSection = namedtuple_with_defaults(
    namedtuple('PersonalUpdateSection',
               [
                   'items',
                   'type',
                   'id',
               ])
)

# Object type for type: 'PERSONAL_UPDATE'
PersonalUpdate = namedtuple_with_defaults(
    namedtuple('PersonalUpdate',
               [
                   'action',
                   'actionTime',
                   'createdAt',
                   'id',
                   'targetUsernames',
                   'targetUsers',
                   'type',
                   'updateIds',
                   'usernames',
                   'users',
               ])
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
