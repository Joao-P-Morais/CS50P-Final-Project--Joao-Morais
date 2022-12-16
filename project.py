from bs4 import BeautifulSoup
import requests
from datetime import timezone
import sys
import datetime
import pytz
from simple_term_menu import TerminalMenu

URL1 = "https://www.theguardian.com/football/fixtures"
URL2 = "https://www.distancelatlong.com/worlds-time-zone/"


def main():

    while True:

        times = get_timezone()
        match = get_match()

        # lines 21 to 31 are responsible for the terminal menu to appear for the user, containing the two options that are presented in the first_menu variable

        first_menu = ["Choose the team to watch: ", "Exit program"]
        terminal_menu = TerminalMenu(first_menu)
        menu_display_choice = terminal_menu.show()

        if first_menu[menu_display_choice] == "Choose the team to watch: ":
            favourite_team = display_teams(match, times)
            country_input = display_countries(times)
            city_input = display_cities(times, country_input)

        elif first_menu[menu_display_choice] == "Exit program":
            sys.exit("Program has ended")

        horas, minutos, ano, mes, dia = get_hour(match[favourite_team][0].split(":"), match[favourite_team][2].split("-"))

        new_time = regulate_timezone_with_match_timezone(country_input, city_input, times, horas, minutos, ano, mes, dia)

        city_no_underscores = city_input.replace("_"," ")

        # line 41 is the culmination of the entire program, as it shows the user information about the match organized in a sentence.

        print(f"\nThe {favourite_team} vs {match[favourite_team][1]} match starts in {diff_time(match, favourite_team)} at {new_time}, {country_input}: {city_no_underscores} time\n")


def display_teams(match, times):

    """
    This function is responsible for the second display appearing after choosing "Choose the team to watch: " in the previous menu.
    This display will show the user all possible teams that are available to watch, in alphabetical order.
    It returns the team that the user chose in the terminal menu.
    """

    title = {"title":"Available teams:"}

    team_menu = sorted(list(match.keys()))

    terminal_menu = TerminalMenu(team_menu, **title)
    menu_entry_teams = terminal_menu.show()

    return team_menu[menu_entry_teams]


def display_countries(dict_times):

    """
    This function is responsible for the third display appearing after choosing the team.
    This display will show the available countries to watch the game, in alphabetical order.
    It returns the country that the user chose in the terminal menu.
    """

    title = {"title":"Available countries to watch the match:"}

    countries_menu = list(dict_times.keys())

    terminal_menu = TerminalMenu(countries_menu, **title)
    menu_entry_countries = terminal_menu.show()

    return countries_menu[menu_entry_countries]


def display_cities(dict_times, country):

    """
    This function is responsible for the last display appearing, where the cities/regions from the chosen country are displayed in alphabetical order.
    It returns the city/region that the user chose in the terminal menu.
    """

    title = {"title":f"Available cities/regions to watch the match in {country}:"}

    cities_menu = sorted(list(dict_times.get(country).keys()))

    terminal_menu = TerminalMenu(cities_menu, **title)
    menu_entry_cities = terminal_menu.show()

    return cities_menu[menu_entry_cities]


def diff_time(match, team):

    """
    This function returns the time difference between the scheduled time of the match in UTC (or BST depending on the time of the year) and the current time, also in UTC (or BST).
    It provides the user with the ability to check how much time is left until the game starts.
    """

    # We use the current timezone of Great Britain (London) since The Guardian website is a UK website so the timezone for the matches will be the same:
    current_utc = (datetime.datetime.now(pytz.timezone("Europe/London")))

    hours_of_match = match.get(team)[0]
    date_of_match = match.get(team)[2]
    match_schedule = date_of_match + " " + hours_of_match
    match_schedule = datetime.datetime.strptime(match_schedule, "%Y-%m-%d %H:%M")

    time_dif = str(match_schedule - current_utc.replace(tzinfo = None)).split(",")

    text = ""

    if len(time_dif) == 2:

    # time_dif(ex.): ["1 Day", " 6:52:12.510197"]

        no_tz = time_dif[1].split(".")
        split_time = no_tz[0].split(":")

        if split_time[0].lstrip() == "0":
            text = time_dif[0] + " and " + split_time[1] + " minutes"
        elif split_time[1] == "0":
            text = time_dif[0] + " and " + split_time [0] + " hours"
        elif split_time[0].lstrip() and split_time[1] == "0":
            text = time_dif[0]
        else:
            text = time_dif[0] + "," + split_time [0] + " hours and " + split_time[1] + " minutes"

        return text

    else:

    # time_dif(ex.): [" 6:52:12.510197"]

        no_tz = str(time_dif).split(".")
        split_time = no_tz[0].split(":")

        if split_time[0].lstrip("['") == "0":
            text = split_time[1].lstrip("0") + " minutes"
        elif split_time[1].lstrip("0") == "":
            text = split_time[0].lstrip("['") + " hours"
        else:
            text = split_time[0].lstrip("['") + " hours and " + split_time[1].lstrip("0") + " minutes"

        return text


def get_match():

    """
    This function returns the "match" dictionary where the key is the matches' home team and the key for the next entry of the dictionary is the away team for the same match.
    It allows the user to get information regarding the match (hour, date and opponent) of the team he/she wants to watch regardless if it is the home or away team.
    """

    try:
        match = {}
        r = requests.get(URL1)
        soup = BeautifulSoup(r.content, "html.parser")

        fixtures = soup.find_all("div", class_="football-matches__day")

        for _ in fixtures:
            date_match = _.find("div", class_="date-divider")
            time_ = date_match.text.strip()
            time_ = str(datetime.datetime.strptime(time_, "%A %d %B %Y")).split(" ")[0]
            table = _.find_all("table", class_= "table table--football football-matches table--responsive-font")

            for cell in table:
                teams = cell.find_all("tr", class_= "football-match football-match--fixture")

                for i in teams:
                    home_team = i.find("div", class_= "football-match__team football-match__team--home football-team")
                    away_team = i.find("div", class_= "football-match__team football-match__team--away football-team")
                    hours_match = i.find("time", class_="js-locale-timestamp")
                    home = home_team.text.strip()
                    away = away_team.text.strip()
                    hours = hours_match.text.strip()
                    date = time_

                    # if the team the user inputs is the matches' home team then append the hours and date of said match, as well as the opposing team onto
                    # the matches dictionary. If the home team already exist in the dicitonary, keep the dictionary as is.
                    # the vice versa happens if the team the user inputs is the matches' away team.

                    if home in match:
                        match[home].append([hours, away, date])
                    else:
                        match[home] = [hours, away, date]

                    if away in match:
                        match[away].append([hours, home, date])
                    else:
                        match[away] = [hours, home, date]

        return match

    except Exception as e:
        print(e)


def get_hour(time_hours, time_year):

    """
    This function returns the exact scheduled time of the match in the UTC time standard, including year, month, day, hour and minutes.
    """

    s_hour, s_minute = time_hours
    s_year, s_month, s_day = time_year

    s_year=int(s_year)
    s_month=int(s_month)
    s_day=int(s_day)
    s_hour=int(s_hour)
    s_minute=int(s_minute)

    # Timezones:
        # BST - British Summer Time
        # GMT - Greenwich Mean Time
    # Time standard:
        # UTC - Universal Coordinated Time

    # From 01:00 (1 AM) on the 27th of March until 01:00 (1 AM) on the 30th of October: UTC = BST-1
    # Any other time throughout the year: UTC = GMT

    d1 = datetime.datetime(s_year, s_month, s_day, s_hour, s_minute)
    d2 = datetime.datetime(s_year, 3, 27, 1, 0)
    d3 = datetime.datetime(s_year, 10, 30, 1, 0)

    if d2 < d1 < d3:
        #utc = bst-1
        utc_match = datetime.datetime(s_year, s_month, s_day, s_hour-1, s_minute)
    else:
        #utc = gmt
        utc_match = d1

    date_match, hour_match = str(utc_match).split(" ")
    hour_utc, minutes_utc, seconds_utc = hour_match.split(":")

    return hour_utc, minutes_utc, s_year, s_month, s_day


def get_timezone():

    """
    This function parses through a timezone website and returns a nested dictionary "cities" where the key-value pair "city" and "time difference from the UTC", respectively,
    The dictionary that is created is in itself a value to the "country" key in the "times" dictionary.
    """
    try:
        times = {}
        r = requests.get(URL2)
        soup = BeautifulSoup(r.content, "html.parser")
        table2 = soup.find("table", class_="table table-striped setBorder")

        for cell in table2.find_all("tbody"):
            rows = cell.find_all("tr")
            for row in rows:
                country = row.find_all("td")[0].text
                city = row.find_all("td")[1].text
                time = row.find_all("td")[2].text

                # if an iteration from the cities list extracted from the website does not exist in the dictionary then add that city to it.
                # else, keep that dictionary the same and continue the iterations.

                if country in times:
                    cities = {city:time}
                    times[country].update(cities)
                else:
                    cities = {city:time}
                    times[country] = cities

        return times

    except Exception as e:
        print(e)


def regulate_timezone_with_match_timezone(country_input, city_input, times, hour_utc, minute_utc, s_year, s_month, s_day):

    """
    If the UTC timezone difference from the scheduled time of the match to the timezone from the country and city of choice is zero (None)
    then the newly set variable (new_time) equals the already established time of the match (date_and_time).
    Else, "new_time" is the time of the match plus/subtracting the UTC time difference from the country and city of choice.
    This function will return the exact scheduled time of the match.
    """

    add_utc = times[country_input].get(city_input)

    # The date_and_time and time_change variables are created as datetime objects so they can be subtracted or added to each other.
    date_and_time = datetime.datetime(s_year, s_month, s_day, int(hour_utc), int(minute_utc))

    if add_utc == "UTC":
       new_time = date_and_time

    else:
        # add_sub_hour is the variable that controls if the hour needs to be subtracted or added
        add_sub_hour = 0
        splited = add_utc.split(" ")
        utc_diff = splited[1]
        first, second = utc_diff.split(":")
        hourz = first.split(first[0])
        add_sub_hour = hourz[1].lstrip("0")

        time_change = datetime.timedelta(minutes = int(second), hours = int(add_sub_hour))


        #if the symbol in the UTC time difference value (first) is a plus sign then add the utc time difference of the country to the time of the match.
        #if it is a minus sign then subtract it.

        if "+" in first:
            new_time = date_and_time + time_change

        if "-" in first:
            new_time = date_and_time - time_change

    return new_time


if __name__ == "__main__":
    main()