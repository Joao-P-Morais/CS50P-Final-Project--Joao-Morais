# When's the game dude? ⚽
###### by João Morais

### Video Demo: [https://youtu.be/ghtBXVRd5EY](https://youtu.be/ghtBXVRd5EY)

🔸 The  `project.py`  file itself has comments to explain some code as well as docstrings for every function that was created.

### Description:

The goal of this project is to create code that finds out when a football (soccer) match is happening, at a specific timezone, given as input the team you want to watch and where in the world you want to watch it.

### How does it work?

- The user simply has to choose 3 answers to each inquiry from the terminal menu:

1. What team to watch.
2. In which country to watch the match.
3. In which city/region from chosen country.

This project uses a parser [\(BeautifulSoup\)](https://beautiful-soup-4.readthedocs.io/en/latest/) to retrieve information from [_The Guardian_ newspaper's website](https://www.theguardian.com/football/fixtures) relating to upcoming football fixtures.
The same parser is used to retrieve information about the [country (and city/region) the match is to be watched in](https://www.distancelatlong.com/worlds-time-zone/), namely the time difference between the timezone of that city/region of the chosen country and the Universal Coordinated Time (UTC).


### Visualization:

The program will print a string to the user with the information about the game, which looks like this:


The **_home team_** vs **_away team_** match starts in **_x days_**, **_x hours_** and **_x minutes_** at **_date and time of the game_**, **_country_** time


⚠️ **Note:** Doesn't matter if the team you are choosing to watch is the home or away team as the program will always return the opposing team.
If the game the user wants to watch is happening that same day, the `x days` variable wont appear in the final string. Similarly if the match starts in minutes, the `x hours` variable won't appear as well.


### File breakdown:

- `project.py` - main code containing all the functions
- `requirements.txt` - list of libraries used
- `test_project.py` - program used to perform unit tests the fucntions of project.py

### Design choices:

Initially this program was parsing a website where the timezone informations where dubious and divided in a variety of tables. I decided to look for a website with correct timezone informations and all comprised in a single table, for easier parsing.

The program was also supposed to ask input from the user regarding team to watch, country to watch and city/region to watch. Although it worked to print the final string with correct information, the user would have to introduce the input exactly as they were displayed in the source's website. So, for example, if the chosen team was Manchester United, the user would have to check _The Guardian_'s website for the exact way the team is written, which would lead to users inputting "Man U" or "Manchester United" as opposed to the site's choice: "Man Utd". The program would then return a string saying "the team is not playing in the upcoming days", which was false. A similar situation would occur when the user would incorrectly input the country's or city/region name. I then decided to create a menu using the [simple_term_menu library](https://pypi.org/project/simple-term-menu/) where the choices for the teams, country and city/region where displayed in the terminal, with the user choosing options with the arrow keys to navigate up and down, leaving no margin for error.

## IMPORTANT NOTE:
During the writing of the code and making of the video, the website I used for the timezones had correct information and I chose this particular website because of the layout (list form) and the fact that the areas were countries and cities as opposed to more cryptic-sounding areas for timezones (e.g., Australian Eastern Standard Time or Central Western Standard Time). Although correct at first, when on the 30th of October the time for the UK and Portugal changed from British Summer Time back to Greenwich Mean Time, the UTC offset time information remained the same, meaning that the code is displaying the game an hour after it is supposed to happen. I tried contacting the owner of the website but got no response.
