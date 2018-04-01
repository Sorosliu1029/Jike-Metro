# -*- coding: utf-8 -*-

"""
wrapper
"""


def repr_namedtuple(nt):
    return nt.__class__.__name__ + '(id={id}, content={content})'.format(id=nt.id, content=nt.content)


def str_namedtuple(nt):
    return nt.__class__.__name__ + '(' + ', '.join(
        '{}={}'.format(k, v) for k, v in zip(nt._fields, nt) if v is not None) + ')'


def namedtuple_with_defaults(namedtuple):
    namedtuple.__new__.__defaults__ = (None,) * len(namedtuple._fields)
    namedtuple.__repr__ = repr_namedtuple
    namedtuple.__str__ = str_namedtuple
    return namedtuple
