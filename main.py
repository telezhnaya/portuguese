import gspread

from getch import getch
from google.oauth2 import service_account
from training_set import create_words_set, print_stats
from utils import *

# Define the scope for accessing Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']


# Define the path to your credentials JSON file
credentials_file = 'credentials.json'

# Define the name of your Google Sheets file
spreadsheet_name = 'Portuguese'
# header:
# palavra	tradução	tipo	tentativas correctas	vice-versa	feito	necessidade	última tentativa correcta	última vice-versa

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scope)

# Authorize and authenticate with Google Sheets
client = gspread.Client(auth=credentials)
client.login()

# print(client.list_spreadsheet_files())
# Open the Google Sheets file
spreadsheet = client.open(spreadsheet_name)
# Select the first sheet in the file
sheet = spreadsheet.get_worksheet(0)
print_stats(sheet)
words_set = create_words_set(sheet)
print("Current set size:", len(words_set))

for i, row in enumerate(words_set):
    from_portuguese = choose_direction(row)
    print()
    question, answer = get_task(row, from_portuguese)
    print("{}/{}\t\t {}".format(i + 1, len(words_set), question))
    input_char = getch()
    if input_char == 's':  # pressed down -> we doubt
        print(answer)
        input_char = getch()
    if input_char == 'w':
        mark_as_done(sheet, row, from_portuguese)
    elif input_char == 'd':  # pressed right -> we know this word
        mark_as_correct(sheet, row, from_portuguese)
    elif input_char == 'a':  # pressed left -> we don't know the word
        mark_as_new(sheet, row, from_portuguese)
    print("Correct:", answer)

sheet.sort((10, 'des'), (6, 'asc'), (1, 'asc'))
