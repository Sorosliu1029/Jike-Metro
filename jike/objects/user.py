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
                   'birthday',
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
                   'qqOpenId',
                   'screenName',
                   'updatedAt',
                   'userId',
                   'username',
                   'usernameSet',
                   'verifyMessage',
                   'wechatOpenId',
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
User.__repr__ = lambda user: 'User(screenName={screenName})'.format(screenName=user.screenName)
