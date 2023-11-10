import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fish_recorder')


def get_user_input(prompt):
    """
    Get input from the user with a specific prompt.
    """
    return input(prompt).strip()


def validate_data_input(response, valid_responses):
    """
    Validating the data provided by the user.
    """
    if response.lower() in valid_responses:
        return True
    else:
        print(f"Invalid response. Please enter one of {valid_responses}.")
        return False


def get_location():
    """
    Retrieves the user's geographical location based of IP address,
    sends a GET request to get latitude, longitude and city from response.
    If request fails returns None for each value and throws an error message.
    """
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data.get("lat"), data.get("lon"), data.get("city")
    except:
        print("Something went wrong fetching your location.")
        return None, None, None


def get_retrieval_speed():
    """
    Asks user if retrieval speed is fast, returns "fast" or "slow" based
    on the user input.
    """
    while True:
        response = get_user_input("Was the retrevial speed fast? (y/n):\n")
        if validate_data_input(response, ['y', 'n']):
            return 'fast' if response.lower() == 'y' else 'slow'


def update_worksheet(data, worksheet_name, column_name):
    """
    Updating the user input to specified column of the worksheet.
    """
    worksheet = SHEET.worksheet(worksheet_name)

    # find all values in row of headings
    headers = worksheet.row_values(1)

    # find the right column
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
    print("Welcome to Fish Recorder")

    # user input
    fish_species = input("Enter your fish species:\n")
    print("Fish species: " + fish_species)
    update_worksheet(fish_species, "input_data", "fish_species")

    retrieval_speed = get_retrieval_speed()
    print("Retrieval speed: " + retrieval_speed)
    update_worksheet(retrieval_speed, "input_data", "retrieval_speed")

    # auto fill
    date, time = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
    update_worksheet(date, "input_data", "date")
    update_worksheet(time, "input_data", "time")

    latitude, longitude, city = get_location()
    # if get_location() throws an error, add null for location variable
    # blank cells would cause an error in data entry (they would occupy the blank cells instead of current row)
    if latitude is None or longitude is None or city is None:
        update_worksheet("null", "input_data", "location")
    else:
        update_worksheet(city, "input_data", "location")
    
    try:
        weather_data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m&hourly=temperature_2m")
        weather_data = weather_data.json()
        c = weather_data['current']
        update_worksheet(c['temperature_2m'], "input_data", "ground_temp")
        update_worksheet(c['cloud_cover'], "input_data", "cloud_cover")
        update_worksheet(c['pressure_msl'], "input_data", "air_pressure")
        update_worksheet(c['wind_direction_10m'], "input_data", "wind_direction")
        update_worksheet(c['wind_speed_10m'], "input_data", "wind_speed")
    except:
        # if api throws error, add null for weather variables so there are no blank cells 
        # blank cells would cause error in data entry (they would occupy the blank cells instead of current row)
        print(f"Oops, something went wrong with the weather data request.")
        update_worksheet('null', "input_data", "ground_temp")
        update_worksheet('null', "input_data", "cloud_cover")
        update_worksheet('null', "input_data", "air_pressure")
        update_worksheet('null', "input_data", "wind_direction")
        update_worksheet('null', "input_data", "wind_speed")


if __name__ == "__main__":
    main()
