# -*- coding: utf-8 -*-

"""
utils
"""

from collections import defaultdict
from .objects.OfficialMessage import OfficialMessage
from .objects.OriginalPost import OriginalPost
from .objects.Question import Question
from .objects.Repost import Repost

converter = defaultdict(dict)
defaultdict.update({
    'OFFICIAL_MESSAGE': OfficialMessage,
    'ORIGINAL_POST': OriginalPost,
    'QUESTION': Question,
    'Repost': Repost,
})
