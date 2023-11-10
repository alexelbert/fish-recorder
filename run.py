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

def get_user_input(promt):
    """
    Get input from the user with a specific promt.
    """
    return input(promt).strip()

def validate_data_input(response, valid_responses):
    """
    Validating the data provided by the user.
    """
    if response.lower() in valid_responses:
        return True
    else:
        print(f"Invalid response. Please enter one of {valid_responses}.")
        return False


def update_worksheet(data, worksheet_name, column_name):
    """
    Updating the user input to specified column of the worksheet.
    """
    worksheet = SHEET.worksheet(worksheet_name)

    # Find all values in row of headings
    headers = worksheet.row_values(1)

    # Find the right column
    try:
        column_index = headers.index(column_name) + 1
    except ValueError:
        print(f"Column '{column_name} not found in worksheet")
        return

    column_values = worksheet.col_values(column_index)
    next_row = len(column_values) + 1

    worksheet.update_cell(next_row, column_index, data)

def main():
    """
    Main function to run the the fish recorder program.
    """
    fish_species = input("Enter your fish species:\n")
    print("Fish species: " + fish_species)
    update_worksheet(fish_species, "input_data", "fish_species")

print("Welcome to Fish Recorder")
main()