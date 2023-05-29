import random

from collections import Counter
from datetime import datetime, timedelta
from enum import Enum
from utils import get_attempts, ENOUGH, REPEAT_AGAIN_AFTER_DAYS


class WordType(Enum):
    KNOWN_OLD = 0
    KNOWN_NEW = 1
    PARTIALLY_KNOWN_MINOR = 2
    PARTIALLY_KNOWN_MAJOR = 3
    NEW = 4


def get_word_type(row):
    a = get_attempts(row, True)
    b = get_attempts(row, False)
    if a >= ENOUGH and b >= ENOUGH:
        d = min(datetime.strptime(row["última tentativa correcta"], "%d.%m.%Y"), datetime.strptime(row["última vice-versa"], "%d.%m.%Y"))
        if d < datetime.now() - REPEAT_AGAIN_AFTER_DAYS:
            return WordType.KNOWN_OLD
        else:
            return WordType.KNOWN_NEW
    if a == 0 and b == 0:
        return WordType.NEW
    return WordType.PARTIALLY_KNOWN_MAJOR if row["necessidade"] else WordType.PARTIALLY_KNOWN_MINOR


def create_words_set(sheet):
    data = [dict(value, **{"index": i + 2}) for i, value in enumerate(sheet.get_all_records())]
    random.shuffle(data)
    # return records

    limits = {WordType.KNOWN_OLD: 1000, WordType.PARTIALLY_KNOWN_MAJOR: 1000, WordType.PARTIALLY_KNOWN_MINOR: 10, WordType.NEW: 10}
    types_count = Counter()

    words_set = []
    for row in data:
        word_type = get_word_type(row)
        if word_type == WordType.KNOWN_NEW:
            continue
        if types_count[word_type] < limits[word_type]:
            types_count[word_type] += 1
            words_set.append(row)
    print("{} old words for today".format(types_count[WordType.KNOWN_OLD]))
    return words_set


def print_stats(sheet):
    print("\tsubstantivos\tverbos\tadjectivos\tfrases\toutros\ttotal")
    words_count = Counter()
    learned_words_count = Counter()
    for value in sheet.get_all_records():
        words_count[value['tipo']] += 1
        if value['feito']:
            learned_words_count[value['tipo']] += 1
    print(f"learned\t{learned_words_count['substantivo']}\t\t{learned_words_count['verbo']}\t{learned_words_count['adjectivo']+learned_words_count['advérbio']}\t\t{learned_words_count['frase']}\t{learned_words_count['outro']}\t{learned_words_count.total()}")
    print(f"total\t{words_count['substantivo']}\t\t{words_count['verbo']}\t{words_count['adjectivo'] + words_count['advérbio']}\t\t{words_count['frase']}\t{words_count['outro']}\t{words_count.total()}")
