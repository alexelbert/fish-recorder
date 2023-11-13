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
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong fetching your location: {e}")
        return None, None, None

def get_fish_size():
    """
    Asks user for the size of the fish in centimeters, validates that it is a number value
    and returns the size as a float value.
    """
    while True:
        response = get_user_input("Enter the size  of the fish in cm:\n")
        try:
            # try and convert response to a positive float value
            size = float(response)
            if size <= 0:
                print("The size must be a positive number. Please try again.")
                continue
            return size
        except ValueError:
            print("Oops. Please enter a number.")


def yes_or_no(question, yes, no):
    """
    Ask the user a yes or no question and returns the response.
    """    
    while True:
        response = get_user_input(f"{question} (y/n):\n")
        if validate_data_input(response, ['y', 'n']):
            return yes if response.lower() == 'y' else no

def get_lure_type():
    """
    Asks the user to select a type of lure from a predefined list and returns the selected type.
    """
    types = ['jig', 'spinner', 'spoon', 'crankbait', 'fly', 'swimbait', 'popper', 'jerkbait']

    while True:
        print("Select a lure type from the following list:\n")
        for i, type in enumerate(types, start=1):
            print(f"{i}. {type}")

        response = get_user_input("Enter the number of your lure type:\n")

        if response.isdigit() and 1 <= int(response) <= len(types):
            return types[int(response) - 1]
        else:
            print("Oops. Please enter a number corresponding to the lure types.\n")

def get_lure_colour():
    """
    Ask the user to input lure color as a string separated by commas.
    Make sure the input is alphanumeric and lowercase,
    as a way of preventing code to be inserted into input.
    """
    while True:
        colours = get_user_input("Enter the colours of the lure, separated by commas:\n").split(',')
        valid_colours = []

        for colour in colours:
            colour = colour.strip().lower()
            if colour.isalnum():
                valid_colours.append(colour)
            else:
                print(f"Invalid colour '{colour}'. Please enter your colours in lowercase seperated by commas.")
                break
        else:
            return ','.join(valid_colours)


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
    print("Welcome to Fish Recorder\n")

    # user input
    fish_species = input("Enter your fish species:\n")
    print("Fish species: " + fish_species)
    update_worksheet(fish_species, "input_data", "fish_species")

    fish_size = get_fish_size()
    print("Fish size: " + str(fish_size) + " cm")
    update_worksheet(fish_size, "input_data", "fish_size")

    water_clarity = yes_or_no('Was the water clear?', 'clear', ' turbid')
    print("Water clarity: " + water_clarity)
    update_worksheet(water_clarity, "input_data", "water_clarity")

    retrieval_speed = yes_or_no('Was the retrieval speed fast?', 'fast', ' slow')
    print("Retrieval speed: " + retrieval_speed)
    update_worksheet(retrieval_speed, "input_data", "retrieval_speed")

    lure_type = get_lure_type()
    print("Lure type: " + lure_type)
    update_worksheet(lure_type, "input_data", "lure_type")

    lure_colour = get_lure_colour()
    print("Lure colour: " + lure_colour)
    update_worksheet(lure_colour, "input_data", "lure_colour")

    # auto fill
    date, time = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
    update_worksheet(date, "input_data", "date")
    update_worksheet(time, "input_data", "time")

    print("Fetching your current location...\n")
    latitude, longitude, city = get_location()
    # if get_location() throws an error, add null for location variable
    # blank cells would cause an error in data entry
    # they would occupy the blank cells instead of current row
    if latitude is None or longitude is None or city is None:
        print("Unable to fetch location, recording 'null' for location.")
        update_worksheet("null", "input_data", "location")
    else:
        print(f"Your location: {city}\n")
        update_worksheet(city, "input_data", "location")

    print("Fetching current weather data...\n")
    try:
        weather_data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m&hourly=temperature_2m")
        weather_data = weather_data.json()
        c = weather_data['current']
        print("Weather data collected. Recording temprature, cloud cover, air preassure, wind speed, wind direction.\n")
        update_worksheet(c['temperature_2m'], "input_data", "ground_temp")
        update_worksheet(c['cloud_cover'], "input_data", "cloud_cover")
        update_worksheet(c['pressure_msl'], "input_data", "air_pressure")
        update_worksheet(c['wind_direction_10m'], "input_data", "wind_direction")
        update_worksheet(c['wind_speed_10m'], "input_data", "wind_speed")
    except requests.exceptions.RequestException as e:
        # if api throws error, add null for variables to avoid blank cells
        # blank cells would cause error in data entry
        # they would occupy the blank cells instead of current row
        print(f"Oops, something went wrong with the weather data request: {e}")
        print("Recodring 'null' for weather data.")
        update_worksheet('null', "input_data", "ground_temp")
        update_worksheet('null', "input_data", "cloud_cover")
        update_worksheet('null', "input_data", "air_pressure")
        update_worksheet('null', "input_data", "wind_direction")
        update_worksheet('null', "input_data", "wind_speed")

    print("All data recorded successfully. Thank you for using Fish Recorder!")


if __name__ == "__main__":
    main()
