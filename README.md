# Fish Recorder

[Visit website here](https://fish-recorder-6d6994a06f94.herokuapp.com)

![Responsive](images/responsive-fish-recorder.png)

Fish Recorder is an interactive Python application designed for sport fishing/hobbyists to record and track details of their fishing trips. This tool helps capture information such as fish species, size, water clarity, lure details and automatically fetches the users location and current weather data. This website was made for educational purposes only.


## UX

### Target Audience

The Fish Recorder application is designed with a specific user group in mind, all inclusive of individuals who are passionate about fishing and have an interest of recording and analysing their fishing experiences. Target group includes:
- Recreational anglers, who enjoy fishing as a leasure activity and want to keep a log of their catches.
- Sport fisherman, competitive anglers who requires detailed records of their fishing to find patterns in order to improve their fishing strategies and success.
- Fishing guides, who maintain detailed records of various fishing trips for reference and teaching purposes.
- Researchers, who study marine environments that can use the data for research on fish behaviour for example.


### Application Logic Flow

The Fish Recorder application follows a intuitive and straightforward flow of logic to ensure ease of use for any angler. Below is an outline involving some key steps used in the application's proccess:

1. Start-Up and Welcome
    - When launched, users are greeted with a welcome message and some brief instructions.
    
    ![Welcome message](images/welcome-message.png)

2. Fish Details Input
    - The user enters details about the fish they caught, includes species and size.

    ![Fish details](images/fish-details.png)

3. Environmental Contitions Input
    - The application prompts the user for information about water clarity and lure retrieval speed.

    ![Enviromental conditions](images/enviromental-conditions.png)

4. Lure Detail Input
    - The user selects lure type from predefined list and input the colour or colours of the lure.

    ![Lure detail input](images/lure-detail.png)

5. Automated Data Collection
    - The application fetches the user's location and weather data automatically.

    ![Automatic data collection](images/automatic-data.png)

6. Data Compilation
    - All the user-provided and fetched data is gathered and compiled into a structured format for recording.
7. Google Sheets Update
    - The compiled data is sent to a Google Sheet, updating the next available row.
8. Completion Confiramtion
    - The user receives confirmation that their data has been recorded successfully.

    ![Confirmation](images/data-compilation.png)

9. Conclusion or Continuation
    - The user can choose to end the session or start a new entry.



## Features

The Fish Recorder application offers a comprehensive suite of features designed to help sport fisherman record and analyze their fishing trips in detail. Following is an overview of it's capabilities:

- Automated Location and Weather Data Retrieval
    - Automatically fetches the user's current geographical location with use of their IP address.
    - Gathers realtime weather data for the user's location, including temperature, cloud cover, air preassure, wind speed and wind direction through an API.

- Interactive user input
    - Prompts user's to specific details of their catch such as species, size, and lure charateristics.
    - Validates user input to ensure accurate and consistent data entry.

- Google Sheets Integration
    - Interacts seemlessly with Google Sheets for efficient data storage and management.
    - Batch updates the worksheet with all recorded data to ensure organized records

- Error handling
    - Implemented error handling for location and weather data retrieval to ensure functionality even if external APIs would fail.



## Technologies Used

The following technologies has been used to make this website work:


- [Python](https://developer.mozilla.org/en-US/docs/Glossary/Python)
    - Core programming language used for developing this application.
- [gspread](https://docs.gspread.org/en/latest/)
    - Is a python library, used for interacting with Google Sheets. Makes the process of "reading from and writing to" simpler.
- [requests](https://docs.python-requests.org/en/latest/index.html)
    - Is a HTTP python library, used for making API calls and fetching location and weather data. 
- [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts)
    - Used for integrating the application with Google Sheets to store the generated data.
- [IP Geolocation API](https://ipgeolocation.io)
    - Used to automatically determine the user's geographical location based on their IP address.
- [Open-Meteo API](https://open-meteo.com/en/docs)
    - Used to fetch real-time weather data, providing the environmental contitions for the aplication.
- [Heroku](dashboard.heroku.com/)
    - Is a cloud platform that enables deployment and hosing of applications. Used to deploy the CLI (Command Line Interface) version of Fish Recorder.
- [GitHub](https://github.com/)
    - Used for storing pushed code.
- [Git](https://git-scm.com/)
    - Used to track changes in the code through  terminal commits and pushing from VS Code to GitHub. 
- [Visual Studio Code](https://code.visualstudio.com)
    - Used as a code editor.
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
    - Extension software used to fix spelling errors across the project.
- [Am I Responsive](http://ami.responsivedesign.is/)
    - Used to make responsive image for README.md file.
- [PEP8 linter](https://pep8ci.herokuapp.com/#)
    - Used to validate python code and check for errors.



## Testing

### User Stories


## Known bugs and fixes


## Deployment


## Credits
 

## Acknowledgements



 