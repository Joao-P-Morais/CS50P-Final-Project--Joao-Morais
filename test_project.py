from project import diff_time
from project import get_match
from project import get_hour
from project import get_timezone
from project import regulate_timezone_with_match_timezone
import datetime
import re


def test_diff_time():

    """
    Checks if function accepts datetime object and gives the proper output.
    For this we should build two regular expressions to check if the return string is being outputted
    in both possible correct formats. For this we assert that if any one the regexes returns not None,
    that a match has occurred and one of the strings is being returned
    assert isinstance is used to check if the return value of the function is a string
    """

    my_time = datetime.datetime.strptime("2022-10-20 20:15:00", "%Y-%m-%d %H:%M:%S")
    my_time2 = datetime.datetime.strptime("2022-11-20 19:00:00", "%Y-%m-%d %H:%M:%S")

    diff_output = diff_time(my_time)

    diff_output2 = diff_time(my_time2)

    regex = re.search(r"[0-9]+ hours and [0-9]+ minutes", diff_output)

    regex2 = re.search(r"[0-9] days, [0-9]+ hours and [0-9]+ minutes", diff_output2)

    assert regex != None or regex2 != None
    assert isinstance(diff_output, str)


def test_get_match():

    """
    Check if the dictionary has any values (line 25)
    Check if the return value is of dict type (line 26)
    """

    assert len(get_match()) > 0
    assert isinstance(get_match(), dict) == True


def test_get_hour():

    """
    Checks if the return value for the scheduled time and date of the match is correct,
    for both timezones where one is an hour less than UTC (BST) for a certain period and the
    other one the same as UTC (GMT) for the the remaining period.
    """

    input_hours = ["19", "00"]
    input_date = ["2022", "10", "19"]
    input_hours2 = ["19", "00"]
    input_date2 = ["2022", "11", "19"]

    assert get_hour(input_hours, input_date) == ('18', '00', 2022, 10, 19)
    assert get_hour(input_hours2, input_date2) == ('19', '00', 2022, 11, 19)

def test_get_timezone():

    """
    Check if the dictionary has any values (line 67)
    Check if the return value is of dict type (line 68)
    """

    assert len(get_timezone()) > 0
    assert isinstance(get_timezone(), dict) == True

def test_regulate_timezone_with_match_timezone():

    """
    Check if the correct value is being returned. For that we need to set that return value as a datetime object
    """

    timezone = get_timezone()

    datetime_dates = datetime.datetime(2022, 10, 20, 19, 30)

    assert regulate_timezone_with_match_timezone("Portugal", "Lisbon", timezone, "18", "30", 2022, 10, 20) == datetime_dates