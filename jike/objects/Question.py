# -*- coding: utf-8 -*-

"""
Object type for type: 'QUESTION'

"""

from collections import namedtuple
from .wrapper import namedtuple_with_defaults
from ..constants import PUBLIC_FIELDS

Question = namedtuple_with_defaults(
    namedtuple('Question',
               list(set(PUBLIC_FIELDS[:] + [
                   'answerCount',
                   'title',
                   'updatedAt',
               ])))
)
