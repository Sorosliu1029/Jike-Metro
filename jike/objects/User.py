# -*- coding: utf-8 -*-

"""
Object type for user

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults

User = namedtuple_with_defaults(
    namedtuple('User',
               [
                   'avatarImage',
                   'bio',
                   'briefIntro',
                   'following',
                   'gender',
                   'isVerified',
                   'profileImageUrl',
                   'ref',
                   'screenName',
                   'statsCount',
                   'updatedAt',
                   'username',
                   'verifyMessage',
               ])
)