# -*- coding: utf-8 -*-

"""
Object type for type: 'REPOST'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import PUBLIC_FIELDS

Repost = namedtuple_with_defaults(
    namedtuple("Repost",
               list(set(PUBLIC_FIELDS[:] + [

               ])))
)
