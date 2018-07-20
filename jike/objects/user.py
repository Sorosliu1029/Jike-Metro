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
                   'createdAt',
                   'following',
                   'gender',
                   'id',
                   'initUsername',
                   'isBanned',
                   'isBetaUser',
                   'isFriendlyUser',
                   'isLoginUser',
                   'isVerified',
                   'medals',
                   'mobilePhoneNumber',
                   'preferences',
                   'profileTags',
                   'province',
                   'profileImageUrl',
                   'ref',
                   'qqOpenId',
                   'qqUserInfo',
                   'school',
                   'screenName',
                   'updatedAt',
                   'userId',
                   'username',
                   'usernameSet',
                   'verifyMessage',
                   'wechatOpenId',
                   'wechatUserInfo',
                   'weiboUid',
                   'weiboUserInfo',
                   'zodiac',

                   'followedCount',
                   'followingCount',
                   'highlightedPersonalUpdates',
                   'liked',
                   'topicCreated',
                   'topicSubscribed',
               ])
)
User.__repr__ = lambda user: 'User(screenName={screenName})'.format(screenName=user.screenName)
