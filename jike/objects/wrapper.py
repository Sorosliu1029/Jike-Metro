# -*- coding: utf-8 -*-

"""
wrapper
"""


def stringify_namedtuple(nt):
    return nt.__class__.__name__ + '(id={id}, content={content})'.format(id=nt.id, content=nt.content)


def namedtuple_with_defaults(namedtuple):
    namedtuple.__new__.__defaults__ = (None,) * len(namedtuple._fields)
    namedtuple.__repr__ = stringify_namedtuple
    return namedtuple
