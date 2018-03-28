# -*- coding: utf-8 -*-

"""
wrappers
"""


def namedtuple_with_defaults(namedtuple):
    namedtuple.__new__.__defaults__ = (None, ) * len(namedtuple._fields)
    return namedtuple
