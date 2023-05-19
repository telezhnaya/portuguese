import gspread
import random

from getch import getch
from google.oauth2 import service_account

ENOUGH = 3
# Define the scope for accessing Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']


# Define the path to your credentials JSON file
credentials_file = 'credentials.json'

# Define the name of your Google Sheets file
spreadsheet_name = 'Portuguese'
# header:
# palavra	tradução	tipo	tentativas correctas	vice-versa	feito

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
sheet.sort((6, 'asc'), (1, 'asc'))

# Get all the values from the sheet
data = [dict(value, **{"index": i + 2}) for i, value in enumerate(sheet.get_all_records())]
random.shuffle(data)


def get_attempts(row, from_portuguese):
    return int(row['tentativas correctas'] if from_portuguese else row['vice-versa'])


def get_task(row, from_portuguese):
    return (row['palavra'], row['tradução']) if from_portuguese else (row['tradução'], row['palavra'])


def get_attempts_cell(from_portuguese):
    return 4 if from_portuguese else 5


def mark_as_done(sheet, row, from_portuguese):
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


def mark_as_new(sheet, row, from_portuguese):
    sheet.update_cell(row['index'], get_attempts_cell(from_portuguese), 0)
    sheet.format("A{0}:F{0}".format(row['index']), {
        "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})


for row in data:
    from_portuguese = random.choice([True, False])
    # 20% chance to see the word I've already learned
    if random.random() > 0.2 and get_attempts(row, from_portuguese) >= ENOUGH:
        continue
    print()
    question, answer = get_task(row, from_portuguese)
    print("\t\t", question)
    input_char = getch()
    if input_char == 'd':  # pressed right -> we know this word
        mark_as_done(sheet, row, from_portuguese)
    elif input_char == 'a':  # pressed left -> we don't know the word
        mark_as_new(sheet, row, from_portuguese)
    elif input_char == 's':  # pressed down -> we doubt
        print(answer)
        input_char = getch()
        if input_char == 'd':  # pressed right -> we know this word
            mark_as_done(sheet, row, from_portuguese)
        elif input_char == 'a':  # pressed left -> we don't know the word
            mark_as_new(sheet, row, from_portuguese)
    print("Correct:", answer)

sheet.sort((6, 'asc'), (1, 'asc'))
