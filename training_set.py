import random

from collections import Counter
from enum import Enum
from utils import get_attempts, ENOUGH


class WordType(Enum):
    KNOWN = 0
    PARTIALLY_KNOWN = 1
    NEW = 2


def get_word_type(row):
    a = get_attempts(row, True)
    b = get_attempts(row, False)
    if a >= ENOUGH and b >= ENOUGH:
        return WordType.KNOWN
    if a == 0 and b == 0:
        return WordType.NEW
    return WordType.PARTIALLY_KNOWN


def create_words_set(sheet):
    data = [dict(value, **{"index": i + 2}) for i, value in enumerate(sheet.get_all_records())]
    random.shuffle(data)
    # return records

    limits = {WordType.KNOWN: 3, WordType.PARTIALLY_KNOWN: 15, WordType.NEW: 5}
    types_count = Counter()

    words_set = []
    for row in data:
        word_type = get_word_type(row)
        if types_count[word_type] < limits[word_type]:
            types_count[word_type] += 1
            words_set.append(row)
    return words_set
