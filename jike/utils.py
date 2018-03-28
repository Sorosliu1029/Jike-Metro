# -*- coding: utf-8 -*-

"""
utils
"""

from .objects.OfficialMessage import OfficialMessage
from .objects.OriginalPost import OriginalPost
from .objects.Question import Question

converter = {
    'OFFICIAL_MESSAGE': OfficialMessage,
    'ORIGINAL_POST': OriginalPost,
    'QUESTION': Question
}
