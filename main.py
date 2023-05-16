import random

import gspread
import sys
import tty
import termios
from google.oauth2 import service_account
from random import choice, shuffle, random


class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x03':
                raise KeyboardInterrupt
            elif ch == '\x04':
                raise EOFError
            elif ch == '\033':
                sys.stdin.read(1)
                ch = sys.stdin.read(1)
                if ch == 'A':
                    ch = 'w'
                elif ch == 'B':
                    ch = 's'
                elif ch == 'C':
                    ch = 'd'
                elif ch == 'D':
                    ch = 'a'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _Getch()

# Define the scope for accessing Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']


# Define the path to your credentials JSON file
credentials_file = 'credentials.json'

# Define the name of your Google Sheets file
spreadsheet_name = 'Portuguese'

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scope)

# Authorize and authenticate with Google Sheets
client = gspread.Client(auth=credentials)
client.login()
#
# print(client.list_spreadsheet_files())
# Open the Google Sheets file
spreadsheet = client.open(spreadsheet_name)

# Select the first sheet in the file
sheet = spreadsheet.get_worksheet(0)

# Get all the values from the sheet
data = [dict(value, **{"index": i + 2}) for i, value in enumerate(sheet.get_all_records())]
shuffle(data)
# sheet.update_cell(2, 3, "abc")


def get_attempts(row, from_portuguese):
    return int(row['tentativas correctas'] if from_portuguese else row['vice-versa'])


def get_task(row, from_portuguese):
    return (row['palavra'], row['tradução']) if from_portuguese else (row['tradução'], row['palavra'])


for row in data:
    from_portuguese = choice([True, False])
    attempts = get_attempts(row, from_portuguese)
    if random() > 0.2 and attempts >= 3:
        continue
    print()
    question, answer = get_task(row, from_portuguese)
    result_cell = 3 if from_portuguese else 4
    print("\t\t", question)
    input_char = getch()
    if input_char == 'd':  # pressed right -> we know this word
        attempts += 1
        sheet.update_cell(row['index'], result_cell, attempts)
        if attempts >= 3:
            print('Congrats, you\'ve learned this!')
            sheet.format("A{0}:D{0}".format(row['index']), {
                "backgroundColor": {
                    "red": 0.8,
                    "green": 1.0,
                    "blue": 0.8
                }})
    elif input_char == 'a':  # pressed left -> we don't know the word
        sheet.update_cell(row['index'], result_cell, 0)
    elif input_char == 's':  # pressed down -> we doubt
        print(answer)
        input_char = getch()
        if input_char == 'd':  # pressed right -> we know this word
            attempts += 1
            sheet.update_cell(row['index'], result_cell, attempts)
            if attempts >= 3:
                print('Congrats, you\'ve learned this!')
                sheet.format("A{0}:D{0}".format(row['index']), {
                    "backgroundColor": {
                        "red": 0.8,
                        "green": 1.0,
                        "blue": 0.8
                    }})
        elif input_char == 'a':  # pressed left -> we don't know the word
            sheet.update_cell(row['index'], result_cell, 0)
    print("Correct:", answer)
