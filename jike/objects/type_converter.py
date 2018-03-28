# -*- coding: utf-8 -*-

"""
convert `type` field to corresponding `object`
"""

from .OfficialMessage import OfficialMessage
from .OriginalPost import OriginalPost
from .Question import Question

converter = {
    'OFFICIAL_MESSAGE': OfficialMessage,
    'ORIGINAL_POST': OriginalPost,
    'QUESTION': Question
}