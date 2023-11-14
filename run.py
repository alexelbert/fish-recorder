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
    Asks user for the size of the fish in centimeters, validates
    that it is a number value and returns the size as a float value.
    """
    while True:
        response = get_user_input("Enter the size of the fish in cm:\n")
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
    Asks the user to select a type of lure from a predefined list
    and returns the selected type.
    """
    types = [
        'jig', 'spinner', 'spoon', 'crankbait', 'fly',
        'swimbait', 'popper', 'jerkbait'
    ]

    print("Select a lure type from the following list:\n")
    for i, type in enumerate(types, start=1):
        print(f"{i}. {type}")

    while True:
        response = get_user_input("Enter the number of your lure type:\n")

        if response.isdigit() and 1 <= int(response) <= len(types):
            return types[int(response) - 1]
        else:
            print("Oops. Please enter a number for your lure type.\n")


def get_lure_colour():
    """
    Ask the user to input lure color as a string separated by commas.
    Make sure the input is alphanumeric and lowercase,
    as a way of preventing code to be inserted into input.
    """
    while True:
        colours = get_user_input(
            "Enter the colours of the lure, separated by commas:\n").split(',')
        valid_colours = []

        for colour in colours:
            colour = colour.strip().lower()
            if colour.isalnum():
                valid_colours.append(colour)
            else:
                print(f"Invalid colour '{colour}'. Please enter your "
                      "colours in lowercase, separated by "
                      "commas.")
                break
        else:
            return ','.join(valid_colours)


def batch_update_worksheet(data, worksheet_name):
    """
    Batch updating the user input in the worksheet.
    """
    worksheet = SHEET.worksheet(worksheet_name)
    # getting all values, count how many there are then add 1 to find next row
    first_empty_row = len(worksheet.get_all_values()) + 1
    # defining range of next row
    cell_list = worksheet.range(f'A{first_empty_row}:N{first_empty_row}')
    # assign user input to corresponding cell object
    for i, cell in enumerate(cell_list):
        if i < len(data):
            cell.value = data[i]

    # update all cell values at once to the spreadsheet
    worksheet.update_cells(cell_list)


def main():
    """
    Main function to run the the fish recorder program.
    """
    print("\nWelcome to Fish Recorder!\n")
    print("This application helps you record details about your "
          "fishing trips\ndetails of your catch and automatically adds "
          "weather conditions and location.")
    print("="*30, "\n")

    # user input
    print("\n--- FISH DETAILS ---\n")
    print("Let's start by recording details about the fish you caught.")
    fish_species = input("Enter your fish species you caught "
                         "(e.g., Trout, Perch):\n")
    print("\nFish species recorded: " + fish_species)

    print("\nNow let's record the size of the fish.")
    fish_size = get_fish_size()
    print("\nFish size recorded: " + str(fish_size) + " cm")

    print("\nNext, let's record the water clarity at the time of your catch.")
    water_clarity = yes_or_no('Was the water clear?', 'clear', 'turbid')
    print("\nWater clarity recorded: " + water_clarity)

    print("\nLet's record the retrieval speed of your lure.")
    retrieval_speed = yes_or_no('Was the retrieval speed fast?',
                                'fast', 'slow')
    print("\nRetrieval speed recorded: " + retrieval_speed)

    print("\nLet's select the type of lure you used.")
    lure_type = get_lure_type()
    print("\n\nLure type recorded: " + lure_type)

    print("\nFinally let's record the color of the lure.")
    lure_colour = get_lure_colour()
    print("\nLure colour recorded: " + lure_colour)

    # auto fill
    date, time = datetime.now().strftime('%Y-%m-%d %H:%M:%S').split()
    print("\n--- LOCATION AND WEATHER DATA ---\n")
    print("Now, we will automatically fetch your current location "
          "and weather data.")
    print("Fetching your current location...\n")
    latitude, longitude, city = get_location()
    # if get_location() throws an error, add null for location variable
    if latitude is None or longitude is None or city is None:
        print("Unable to fetch location, recording 'null' for location.")
    else:
        print(f"Your location: {city}\n")

    print("Fetching current weather data...\n")
    try:
        weather_data = requests.get(
         f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&"
         f"longitude={longitude}&current=temperature_2m,precipitation,"
         f"weather_code,cloud_cover,pressure_msl,wind_speed_10m,"
         f"wind_direction_10m&hourly=temperature_2m"
        )
        weather_data = weather_data.json()
        c = weather_data['current']
        print("Weather data collected. Recording temperature, cloud cover, "
              "air pressure, wind speed, wind direction.\n")
        temperature = c['temperature_2m']
        cloud_cover = c['cloud_cover']
        pressure = c['pressure_msl']
        wind_direction = c['wind_direction_10m']
        wind_speed = c['wind_speed_10m']

    except requests.exceptions.RequestException as e:
        # if API throws error, add null for variables to avoid blank cells
        print(f"Oops, something went wrong with the weather data request: {e}")
        print("Recording 'null' for weather data.")
        temperature = 'null'
        cloud_cover = 'null'
        pressure = 'null'
        wind_direction = 'null'
        wind_speed = 'null'

    data = [
        date, time, city, temperature, cloud_cover, pressure,
        wind_direction, wind_speed, fish_species, fish_size,
        water_clarity, lure_type, lure_colour, retrieval_speed
    ]
    print("Recording your data to the worksheet...")
    batch_update_worksheet(data, "input_data")
    print("\n--- DATA RECORDED SUCCESSFULLY ---\n")

    print("Thank you for using Fish Recorder!")
    print("Your fishing trip details have been successfully recorded.")


if __name__ == "__main__":
    main()
