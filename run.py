import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fish_recorder')


def update_worksheet(fish_species, worksheet_name):
    """
    Updating the user input for fish species into the worksheet
    """
    
    worksheet = SHEET.worksheet(worksheet_name)

    # Find all values in header row
    headers = worksheet.row_values(1)

    # find the column named "fish species"
    try:
        fish_species_col = headers.index('fish_species') + 1
    except ValueError:
        raise ValueError("Column 'fish_species' not found in the worksheet.")

    fish_species_col_values = worksheet.col_values(fish_species_col)
    next_row = len(fish_species_col_values) + 1

    worksheet.update_cell(next_row, fish_species_col, fish_species)

fish_species = input("Enter your fish species:")
print("Fish species: " + fish_species)
update_worksheet(fish_species, "input_data")





# Write your code to expect a terminal of 80 characters wide and 24 rows high
