import random

from datetime import date, datetime, timedelta


ENOUGH = 3
REPEAT_AGAIN_AFTER_DAYS = timedelta(days=150)
FROM_PT_COUNT = 'de português para inglês'
FROM_EN_COUNT = 'de inglês para português'
CHOOSE_TO_LEARN_CELL = 10


def get_attempts(row, from_portuguese):
    return int(row[FROM_PT_COUNT] if from_portuguese else row[FROM_EN_COUNT])


def get_task(row, from_portuguese):
    return (row['palavra'], row['tradução']) if from_portuguese else (row['tradução'], row['palavra'])


def get_attempts_cell(from_portuguese):
    return 4 if from_portuguese else 5


def get_last_date_checked_cell(from_portuguese):
    return 8 if from_portuguese else 9


def choose_direction(row):
    if row[FROM_PT_COUNT] - row[FROM_EN_COUNT] >= 2 or \
            datetime.now() - datetime.strptime(row["última vice-versa"], "%d.%m.%Y") > REPEAT_AGAIN_AFTER_DAYS:
        return False
    if row[FROM_EN_COUNT] - row[FROM_PT_COUNT] >= 2 or \
            datetime.now() - datetime.strptime(row["última tentativa correcta"], "%d.%m.%Y") > REPEAT_AGAIN_AFTER_DAYS:
        return True
    return random.choice([True, False])


def mark_as_correct(sheet, row, from_portuguese):
    attempts = get_attempts(row, from_portuguese) + 1
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), attempts)
    sheet.update_cell(row['index'], get_last_date_checked_cell(from_portuguese), date.today().strftime("%d.%m.%Y"))
    if attempts >= ENOUGH and get_attempts(row, not from_portuguese) >= ENOUGH:
        print('Congrats, you\'ve learned this!')
        sheet.update_cell(row['index'], CHOOSE_TO_LEARN_CELL, '')
        sheet.format("A{0}:G{0}".format(row['index']), {
            "backgroundColor": {
                "red": 0.8,
                "green": 1.0,
                "blue": 0.8
            }})


def mark_as_done(sheet, row, from_portuguese):
    attempts = max(ENOUGH, get_attempts(row, from_portuguese) + 1)
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), attempts)
    sheet.update_cell(row['index'], get_last_date_checked_cell(from_portuguese), date.today().strftime("%d.%m.%Y"))
    if get_attempts(row, not from_portuguese) >= ENOUGH:
        print('Congrats, you\'ve learned this!')
        sheet.format("A{0}:G{0}".format(row['index']), {
            "backgroundColor": {
                "red": 0.8,
                "green": 1.0,
                "blue": 0.8
            }})


def mark_as_new(sheet, row, from_portuguese):
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), 0)
    sheet.format("A{0}:G{0}".format(row['index']), {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})
