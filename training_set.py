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

    limits = {WordType.KNOWN: 3, WordType.PARTIALLY_KNOWN: 24, WordType.NEW: 3}
    types_count = Counter()

    words_set = []
    for row in data:
        word_type = get_word_type(row)
        # Help myself to finish learning important words
        if (row['necessidade'] and word_type != WordType.KNOWN) or types_count[word_type] < limits[word_type]:
            types_count[word_type] += 1
            words_set.append(row)
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
