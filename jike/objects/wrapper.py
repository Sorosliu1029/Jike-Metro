# -*- coding: utf-8 -*-

"""
wrapper
"""


def stringify_namedtuple(nt):
    return nt.__class__.__name__ + '(' + ', '.join(
        '{}={}'.format(k, v) for k, v in zip(nt._fields, nt) if v is not None) + ')'


def namedtuple_with_defaults(namedtuple):
    namedtuple.__new__.__defaults__ = (None,) * len(namedtuple._fields)
    namedtuple.__repr__ = stringify_namedtuple
    return namedtuple
