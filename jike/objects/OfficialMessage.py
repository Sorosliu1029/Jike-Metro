# -*- coding: utf-8 -*-

"""
Object type for type: 'OFFICIAL_MESSAGE'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import PUBLIC_FIELDS

OfficialMessage = namedtuple_with_defaults(
    namedtuple('OfficialMessage',
               list(set(PUBLIC_FIELDS + [
                   'abstract',
                   'video',
               ])))
)
