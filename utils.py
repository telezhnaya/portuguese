ENOUGH = 3


def get_attempts(row, from_portuguese):
    return int(row['tentativas correctas'] if from_portuguese else row['vice-versa'])


def get_task(row, from_portuguese):
    return (row['palavra'], row['tradução']) if from_portuguese else (row['tradução'], row['palavra'])


def get_attempts_cell(from_portuguese):
    return 4 if from_portuguese else 5


def mark_as_correct(sheet, row, from_portuguese):
    attempts = get_attempts(row, from_portuguese) + 1
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), attempts)
    if attempts >= ENOUGH and get_attempts(row, not from_portuguese) >= ENOUGH:
        print('Congrats, you\'ve learned this!')
        sheet.format("A{0}:F{0}".format(row['index']), {
            "backgroundColor": {
                "red": 0.8,
                "green": 1.0,
                "blue": 0.8
            }})


def mark_as_done(sheet, row, from_portuguese):
    attempts = max(ENOUGH, get_attempts(row, from_portuguese) + 1)
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), attempts)
    if get_attempts(row, not from_portuguese) >= ENOUGH:
        print('Congrats, you\'ve learned this!')
        sheet.format("A{0}:F{0}".format(row['index']), {
            "backgroundColor": {
                "red": 0.8,
                "green": 1.0,
                "blue": 0.8
            }})


def mark_as_new(sheet, row, from_portuguese):
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), 0)
    sheet.format("A{0}:F{0}".format(row['index']), {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})
