# -*- coding: utf-8 -*-

"""
Object type for type: 'ORIGINAL_POST'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import PUBLIC_FIELDS

OriginalPost = namedtuple_with_defaults(
    namedtuple('OriginalPost',
               list(set(PUBLIC_FIELDS[:] + [
                   'messageId',
                   'poi',
               ])))
)
