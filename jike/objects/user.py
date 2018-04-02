# -*- coding: utf-8 -*-

"""
Object type for user

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import ENDPOINTS

User = namedtuple_with_defaults(
    namedtuple('User',
               [
                   'areaCode',
                   'avatarImage',
                   'backgroundImage',
                   'bio',
                   'briefIntro',
                   'city',
                   'country',
                   'following',
                   'gender',
                   'id',
                   'initUsername',
                   'isBetaUser',
                   'isLoginUser',
                   'isVerified',
                   'mobilePhoneNumber',
                   'preferences',
                   'province',
                   'profileImageUrl',
                   'ref',
                   'screenName',
                   'updatedAt',
                   'userId',
                   'username',
                   'usernameSet',
                   'verifyMessage',
                   'weiboUid',
                   'weiboUserInfo',

                   'followedCount',
                   'followingCount',
                   'highlightedPersonalUpdates',
                   'liked',
                   'topicCreated',
                   'topicSubscribed',
               ])
)
User.__repr__ = lambda user: 'User(id={id}, screenName={screenName})'.format(id=user.id, screenName=user.screenName)
