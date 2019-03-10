# Imports.
import datetime
import re

import io_utils
import wl_resource

"""---------------------------------------------------------------------
    Contains date- and time-related functions.
   ---------------------------------------------------------------------
"""


def calc_duration_abs(string):
    """-----------------------------------------------------------------
        Parses a string and determines the duration it describes, if
         possible.

        Arguments:
        - string -- the string to parse.

        Returns:  a timedelta object if a valid duration is found; else
         None.
       -----------------------------------------------------------------
    """
    # The string must contain one or more number/word pairs:  a number
    #  (or number phrase) and a unit of measure.  These should (but need
    #  not be) in descending order.
    # First, convert any numbers.
    raw_list = wl_resource.numbers(string)
    # Then cull unneeded elements from the list.
    word_list = []
    for word in raw_list:
        if not (word == None or str(word).lower() == "and"):
            word_list.append(word)
        # end if
    # end for
    # Now move through the string from left to right.
    minutes = None
    hours = None
    days = None
    ndx = 0
    while ndx < len(word_list):
        amt = 0
        # An inner loop adds numbers together.  If there aren't any,
        #  amt will remain 0.
        while (
          type(word_list[ndx]) in [int, float]) and (ndx < len(word_list)):
            amt += word_list[ndx]
            ndx += 1
        # end while
        # If there was no amount, check for an unspaced number/unit
        #  combination.
        if not amt:
            if re.fullmatch(r"\d+m", word_list[ndx]):
                minutes = int(re.match(r"\d+", word_list[ndx]).group())
                ndx += 1
                continue
            if re.fullmatch(r"\d+h", word_list[ndx]):
                hours = int(re.match(r"\d+", word_list[ndx]).group())
                ndx += 1
                continue
            if re.fullmatch(r"\d+d", word_list[ndx]):
                days = int(re.match(r"\d+", word_list[ndx]).group())
                ndx += 1
                continue
            # Otherwise just move to the next word.
            ndx += 1
            continue
        # end if
        # Determine the units (if not valid, just move to the next
        #  word).
        if re.match(r"m\w*", word_list[ndx]):
            minutes = amt
        elif re.match(r"h\w*", word_list[ndx]):
            hours = amt
        elif re.match(r"d\w*?", word_list[ndx]):
            days = amt
        # end if
        ndx += 1
    # end while
    # Having gone through the list, see if any times were found.  If not
    #  return None.
    if (minutes == None) and (hours == None) and (days == None):
        return None
    # end if
    # Change non-present units to zeroes.
    if not minutes:
        minutes = 0
    # end if
    if not hours:
        hours = 0
    # end if
    if not days:
        days = 0
    # end if
    # Return a timedelta created from the times found.  Note that zero
    #  minutes is a valid duration.
    return datetime.timedelta(days=days, hours=hours, minutes=minutes)
# end function


def calc_duration_rel(end_time, start_time):
    """-----------------------------------------------------------------
        Determines a duration based on two times.

        Arguments:
        - end_time -- the ending time.
        - start_time -- the starting time.

        Returns:  a timedelta object representing the difference between
         the two times, if that difference is positive; else None.
       -----------------------------------------------------------------
    """
    # Subtract the start time from the end time.  (Note that if a
    #  task extends across more than one day, the duration must be
    #  entered directly.)
    if end_time >= start_time:
        # Create timedeltas for subtraction.
        end_td = datetime.timedelta(
          hours=end_time.hour, minutes=end_time.minute)
        start_td = datetime.timedelta(
          hours=start_time.hour, minutes=start_time.minute)
        # Return the resulting timedelta.
        return end_td - start_td
    else:
        msg = "The end time cannot be before the start time."
        wl_resource.print_status("error", msg)
        return None
    # end if
# end function


def conv_wkday(day, iso=False):
    """-----------------------------------------------------------------
        Converts a weekday obtained from a date object's weekday (or
         isoweekday) method, which is Monday-based, to a Sunday-based
         weekday.

        Arguments:
        - day -- the weekday to convert.

        Keyword Arguments:
        - iso -- Set if the isoweekday method was used (default False).

        Returns:  an integer between 1 (Sunday) and 7 (Saturday).
       -----------------------------------------------------------------
    """
    # Apply the correct formula and return the result.
    if iso:
        if day == 7:
            return 1
        else:
            return day + 1
        # end if
    else:
        if day == 6:
            return 1
        else:
            return day + 2
    # end if
# end function


def dformat(date, endian):
    """-----------------------------------------------------------------
        Takes a date and formats it accoring to the correct endian.

        Arguments:
        - date -- the date object to convert.
        - endian -- the work log object's endian attribute.

        Returns:  a string representing the date.
       -----------------------------------------------------------------
    """
    # Return a string in the proper format.
    if endian == "B":
        return date.strftime("%Y/%m/%d")
    elif endian == "M":
        return date.strftime("%m/%d/%Y")
    else:
        return date.strftime("%d/%m/%Y")
    # end if
# end function


def find_weekday(day, ordinal, month, year):
    """-----------------------------------------------------------------
        Determines the date of the month on which a specific day of the
         week falls.

        Keyword Arguments:
        - day -- the day of the week to find.
        - ordinal -- which week to find.
        - month -- the month in which to search.
        - year -- the year in which to search.

        Returns:  a date object representing the correct day, or None if
         the specified day does not occur within the specified month.
       -----------------------------------------------------------------
    """
    # First determine the weekday on which the specified month starts.
    first_day = conv_wkday(datetime.date(year, month, 1).weekday())
    # Apply the correct formula to find the date.
    if day == first_day:
        date = 1 + (ordinal - 1) * 7
    elif day > first_day:
        date = 1 + day - first_day + (ordinal - 1) * 7
    else:
        date = 1 + (7 - (first_day - day)) + (ordinal - 1) * 7
    # end if
    # Attempt to return a date object with the date found.  If it falls
    #  outside the range of that particular month, return None.
    try:
        return datetime.date(year, month, date)
    except ValueError:
        return None
    # end try
# end function


def last_date(month, year):
    """-----------------------------------------------------------------
        Returns the last date of a given month.

        Arguments:
        - month -- the month to check.
        - year -- the year to check.

        Returns:  an integer between 28 and 31, representing the last
         date of the specified month.
       -----------------------------------------------------------------
    """
    # Standard months.
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    # February.
    else:
        # Rather than re-creating a complex formula, just try to create
        #  a date object for Febuary 29 and see if it works.
        try:
            datetime.date(year, month, 29)
            return 29
        except ValueError:
            return 28
        # end try
    # end if
# end function


def parse_date_calendar(wl_obj, word_list):
    """-----------------------------------------------------------------
        Parses a word list to see if it contains a date with either
         the month or day spelled out.

        Arguments:
        - wl_obj -- the work log object.
        - word_list -- the list of words to parse.

        Returns:  a date object if successful; else None.
       -----------------------------------------------------------------
    """
    # Check all the elements in every order.  If one matches, set the
    #  work log object's date_format attribute and return the date
    #  object.
    if len(word_list) == 2:
        # Month and day.  Note--don't set the date format here, becuase
        #  it could be either big-endian or middle-endian.
        good = _check_calendar_date(word_list[0], word_list[1])
        if good:
            return good
        # end if
        # Day and month.
        good = _check_calendar_date(word_list[1], word_list[0])
        if good:
            wl_obj.date_format = "L"
            return good
        # end if
    elif len(word_list) == 3:
        # Month, day and year.
        good = _check_calendar_date(
          word_list[0], word_list[1], year=word_list[2])
        if good:
            wl_obj.date_format = "M"
            return good
        # end if
        # Day, month and year.
        good = _check_calendar_date(
          word_list[1], word_list[0], year=word_list[2])
        if good:
            wl_obj.date_format = "L"
            return good
        # end if
        # Year, month and day.
        good = _check_calendar_date(
          word_list[1], word_list[2], year=word_list[0])
        if good:
            wl_obj.date_format = "B"
            return good
        # end if
    # end if
    # If nothing worked, return None.
    return None
# end function


def parse_date_input(wl_obj, string):
    """-----------------------------------------------------------------
        Parses input from the user which should contain a date, and
         extracts the date.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, else None.
       -----------------------------------------------------------------
    """
    # If the string is a standard numeric date, check to make sure it is
    #  valid.  The result will either be a date object or None.
    if re.search(r"^\d{1,4}[-/.]{1}\d{1,4}[-/.]?\d{1,4}$", string):
        return parse_date_numeric(wl_obj, string)
    # Otherwise check to see if it is a valid word date.  The result
    #  will still be a date object or None.
    else:
        return parse_date_phrase(wl_obj, string)
    # end if
# end function


def parse_date_numeric(wl_obj, string):
    """-----------------------------------------------------------------
        Function that checks to make sure a standard date entry is
         actually a valid date, and allows the date format to be changed
         if it isn't.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    # Format constants.
    BIG_FORMAT = "%Y %B %d"
    MID_FORMAT = "%B %d, %Y"
    LIT_FORMAT = "%d %B %Y"
    # First separate the elements of the date and convert them to
    #  integers.
    numbers = re.findall(r"\d+", string)
    for x, number in enumerate(numbers):
        numbers[x] = int(number)
    # end for
    # If there are only two elements, the year was omitted and defaults
    #  to the current year.  Where the year element is inserted depends
    #  on the format.
    if len(numbers) == 2:
        if wl_obj.date_format == "B":
            numbers.insert(0, datetime.date.today().year())
        else:
            numbers.append(datetime.date.today().year())
        # end if
    # end if
    # Now try to create a date object with the selected format.
    entry_date = _create_date(numbers, wl_obj.date_format)
    # If it's valid, return it.
    if entry_date:
        return entry_date
    # If it's not valid, try the other formats.
    valid_formats, valid_dates = _check_other_endians(
      numbers, wl_obj.date_format)
    # If neither of the other formats is valid, just return None.
    if valid_formats == []:
        wl_resource.print_status(
          "error", msg=f"{string} could not be interpreted as a valid date.")
        return None
    # end if
    # Otherwise, inform the user of the successful format(s) and ask if
    #  he/she wants to change the selected format to match, or re-enter
    #  the date.
    msg = io_utils.print_block(
      f"The date {string} is not valid in the currently selected format, " +
      "but is valid in a different format.  You can choose to change the " +
      "date format or re-enter the date for this task.", str_=True)
    wl_resource.print_status("warning", msg=msg)
    option_list = []
    for x, ndn in enumerate(valid_formats):
        if ndn == "B":
            option_list.append(valid_dates[x].strftime(BIG_FORMAT))
        elif ndn == "M":
            option_list.append(valid_dates[x].strftime(MID_FORMAT))
        else:
            option_list.append(valid_dates[x].strftime(LIT_FORMAT))
            # end if
        # end if
    # end for
    option_list.append("Re-enter the date.")
    # Give the user the option to change the format or try again.
    response = io_utils.menu(option_list, keystroke_list="#", quit=False)
    # If the user chose to try again, return None.
    if response == len(option_list):
        input("Press «ENTER» to continue.")
        return None
    # Otherwise, reset the date format and return the date object.
    else:
        wl_obj.date_format = valid_formats[response - 1]
        return valid_dates[response - 1]
    # end if
# end function


def parse_date_phrase(wl_obj, string):
    """-----------------------------------------------------------------
        Function that checks a string to see if it contains a valid word
         date.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    # First break the string into a list of words.
    word_list = re.findall(r"\b\w+\b", string)
    # If the user included the words "the" or "of", discard it.
    s = []
    for word in word_list:
        if word.lower() != "the" and word.lower() != "of":
            s.append(word)
        # end if
    # end for
    word_list = s
    # Check according to the length of the string.
    if len(word_list) == 1:
        # There are three valid one-word responses, plus the days of the
        #  week.
        if word_list[0].lower() == "today":
            return datetime.date.today()
        elif word_list[0].lower() == "yesterday":
            return datetime.date.today() - datetime.timedelta(days=1)
        elif word_list[0].lower() == "tomorrow":
            return datetime.date.today() + datetime.timedelta(days=1)
        else:
            valid = wl_resource.weekday(word_list[0])
            # If the string is a day of the week, return the date object
            #  that corresponds to that day of the current week.  Else
            #  return None.
            if valid:
                return _create_date_from_weekday(valid, 0)
            else:
                wl_resource.print_status(
                  "error", msg=f"{string} could not be interpreted as a " +
                  "valid date.")
                return None
            # end if
        # end if
    elif len(word_list) == 2:
        # A two-word response can be a calendar date without the year,
        #  or a phrase.  Check for a calendar date first.
        good = parse_date_calendar(wl_obj, word_list)
        if good:
            return good
        # end if
        # Two-word date phrases all start with "this", "next", or
        #  "last", followed by a day of the week.
        if word_list[0].lower() == "this":
            offset = 0
        elif word_list[0].lower() == "last":
            offset = -1
        elif word_list[0].lower() == "next":
            offset = 1
        else:
            wl_resource.print_status(
              "error", msg=f"{string} could not be interpreted as a valid " +
              "date.")
            return None
        # end if
        valid = wl_resource.weekday(word_list[1])
        if valid:
            return _create_date_from_weekday(valid, offset)
        else:
            wl_resource.print_status(
              "error", msg=f"{string} could not be interpreted as a valid " +
              "date.")
            return None
        # end if
    elif len(word_list) == 3:
        # Three word calendar dates are a full month, day and year (but
        #  not necessarily in that order).  Check for them.
        good = parse_date_calendar(wl_obj, word_list)
        if good:
            return good
        # end if
        # There are two set three-word date phrases.  It's simpler to
        #  search for them in the original string.
        if re.search(r"day after tomorrow", string, re.I):
            return datetime.date.today() + datetime.timedelta(days=2)
        elif re.search(r"day before yesterday", string, re.I):
            return datetime.date.today() - datetime.timedelta(days=2)
        # end if
        # Other three-word date phrases are a day of the week followed
        #  by either "before last" or "after next".
        valid = wl_resource.weekday(word_list[0])
        if valid:
            if (
              word_list[1].lower() == "before" and
              word_list[2].lower() == "last"):
                return _create_date_from_weekday(valid, -2)
            elif (
              word_list[1].lower() == "after" and
              word_list[2].lower() == "next"):
                return _create_date_from_weekday(valid, 2)
            else:
                wl_resource.print_status(
                  "error", msg=f"{string} could not be interpreted as a " +
                  "valid date.")
                return None
            # end if
        else:
            wl_resource.print_status(
              "error", msg=f"{string} could not be interpreted as a valid " +
              "date.")
            return None
        # end if
    else:
        wl_resource.print_status(
          "error", msg=f"{string} could not be interpreted as a valid date.")
        return None
    # end if
# end function


def parse_duration_input(wl_obj, entry, string):
    """-----------------------------------------------------------------
        Function that checks a string to see if it contains a valid
         duration or end time, and calculates the duration from an end
         time if necessary.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.
        - string -- the user input.

        Returns:  a timedelta object if successful, or None.
       -----------------------------------------------------------------
    """
    # First just check to see if it's a end time.
    end_time = parse_time_input(wl_obj, string)
    # If it is a time, send to the function to calculate the duration.
    if end_time:
        return calc_duration_rel(end_time, entry.time)
    # end if
    # Otherwise, send to the function to construct the duration from
    #  the string.
    return calc_duration_abs(string)
# end function


def parse_time_input(wl_obj, string):
    """-----------------------------------------------------------------
        Function that preprocesses a string which is supposed to contain
         a valid time, and passes the input to a validator function
         which will create a time object from it if possible.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a time object if successful, or None.
       -----------------------------------------------------------------
    """
    # First search the entire string for an AM/PM marker.
    pm = None
    if re.search(r"([\d|\s]a[.]?m?[.]?$)|(morning)", string):
        wl_obj.time_format = 12
        pm = False
    elif re.search(
      r"([\d|\s]p[.]?m?[.]?$)|(afternoon)|(evening)|(night)", string):
        wl_obj.time_format = 12
        pm = True
    # end if
    word_list = []
    # If the string is all numbers (with or without a colon) it can be
    #  processed directly.
    if re.match(r"\d{1,2}:?\d{0,2}\s?[a|p]?\.?m?\.?$", string):
        num_list = re.split(r"\D", string)
        # if the first number is 3-4 digits, it can only be a complete
        #  time.  If it is 1-2 digits, it must be an hour, and minutes
        #  may follow.
        # If a valid time in 24-hour format is entered, the pm flag is
        #  ignored and the time_format attribute reset to 24.
        # Ambiguous times in 12-hour format are assumed to be AM unless
        #  the pm flag is set.
        if int(num_list[0]) > 99:
            # Break the first element into hour and minute segments
            #  (discard the rest of the string).  Pass these to the
            #  validating function to return a time object or None.
            word_list.append(int(num_list[0]) // 100)
            word_list.append(int(num_list[0]) % 100)
            return _create_time(wl_obj, word_list, pm)
        else:
            # If the hour and minute elements are already separated,
            #  just pass the original list to the validator.
            return _create_time(wl_obj, num_list, pm)
        # end if
    # end if
    # If the time isn't in a standard format...
    # Break the input string into units.
    raw_list = string.split(" ")
    # Process each raw unit.
    for raw_word in raw_list:
        # First separate any letter/number combinations.
        raw_word_list = re.findall(r"\D+|\d+", raw_word)
        # If there aren't any combos, this will be a one-item list.
        for element in raw_word_list:
            # Add to the final word list either the word or its integer
            #  equivalent.
            word_list.append(wl_resource.cardinal(element))
        # end for
    # end for
    # With all numeric strings and number words converted to integers,
    #  return either a time object or None.
    return _create_time(wl_obj, word_list, pm)
# end function


def set_endian(wl_obj):
    """-----------------------------------------------------------------
        Function which asks the user to set the format for dates to be
         entered and displayed.

        Arguments:
        - wl_obj -- the work log object.

        Modifies:  the work log object's date_format attribute.

        Returns:  nothing
       -----------------------------------------------------------------
    """
    # Print explanation.
    wl_resource.print_status(
      "status", msg="The date format has not been set.", go=True)
    # Set the list of date format to choose from.
    menu_list = [
      "July 15, 2010 (7/15/10)", "15 July, 2010 (15/7/10)",
      "2010 July 15 (10/7/15)"]
    # Get the user to pick one.
    response = io_utils.menu(
      menu_list, keystroke_list="#", confirm=True, quit=False,
      prompt="Please select your preferred date format:")
    if response == 1:
        wl_obj.date_format = "M"
    elif response == 2:
        wl_obj.date_format = "L"
    elif response == 3:
        wl_obj.date_format = "B"
    # end if
    return
# end function


def _check_calendar_date(month, day, year=None):
    """-----------------------------------------------------------------
        Checks two or three words to see if they form a valid calendar
         date.

        Arguments:
        - month -- the word representing the month.
        - day -- the word representing the day.

        Keyword Arguments:
        - year -- the word representing the year.

        Returns:  a date object if successful; else None.
       -----------------------------------------------------------------
    """
    m = wl_resource.month(month)
    if m:
        try:
            d = int(day)
        except ValueError:
            d = wl_resource.ordinal(day)
        # end try
        if d:
            if not year:
                y = datetime.date.today().year
            else:
                try:
                    y = int(year)
                    if not (1900 <= y <= 2100):
                        return None
                    # end if
                except ValueError:
                    return None
                # end try
            # end if
            return datetime.date(y, m, d)
        else:
            return None
        # end if
    else:
        return None
    # end if
# end function


def _check_other_endians(numbers, endian):
    """-----------------------------------------------------------------
        Checks the validity of a potential date against the two formats
         which are NOT currently selected.

        Arguments:
        - numbers -- the numbers that form the potential date.
        - endian -- the date format to NOT test.

        Returns:  a list of zero to two characters indicating for which
         formats the numbers form a valid date (if any), and a list of
         corresponding date objects.
       -----------------------------------------------------------------
    """
    endian_list = []
    date_list = []
    for ndn in ["L", "M", "B"]:
        # Only test if not the current format.
        if ndn != endian:
            # If the create date function returns something, add the
            #  corresponding endian.
            date = _create_date(numbers, ndn)
            if date:
                endian_list.append(ndn)
                date_list.append(date)
            # end if
        # end if
    # end for
    return endian_list, date_list
# end function


def _create_date(numbers, endian):
    """-----------------------------------------------------------------
        Helper function that tries to create a date from a set of
         numbers.

        Arguments:
        - numbers -- the numbers that form the potential date.
        - endian -- the date format.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    # Aliases.
    if endian == "B":
        year = 0
        month = 1
        day = 2
    elif endian == "M":
        month = 0
        day = 1
        year = 2
    else:
        day = 0
        month = 1
        year = 2
    # end if
    # The year may be abbreviated.  If it is, expand it to a year
    #  between 1950 and 2049.  (Note that this range only applies to
    #  abbreviated years.  4-digit years can be between 1900 and 2099.)
    if numbers[year] < 100:
        if numbers[year] > 49:
            numbers[year] += 1900
        else:
            numbers[year] += 2000
        # end if
    # end if
    # Try to create a date object with the numbers.
    try:
        return datetime.date(numbers[year], numbers[month], numbers[day])
    except ValueError:
        return None
    # end try
# end function


def _create_date_from_weekday(weekday, offset):
    """-----------------------------------------------------------------
        Helper function which creates a date given a day of the week.

        Arguments:
        - weekday -- the day of the week for which to create the date.
        - offset -- the week in which to create the date.

        Returns:  a date object.
       -----------------------------------------------------------------
    """
    # First, identify the current weekday.
    current_day = datetime.date.today().isoweekday()
    # Adjust from a Monday-based week to a Sunday-based week.
    if current_day < 7:
        current_day += 1
    else:
        current_day = 1
    # end if
    # Determine the difference between the current weekday and the
    #  weekday to be used.
    day_offset = weekday - current_day
    # Convert the week offset to days.
    week_offset = offset * 7
    # Use timedeltas to create and return the date object.
    return (
      datetime.date.today() + datetime.timedelta(days = day_offset) +
      datetime.timedelta(days = week_offset))
# end function


def _create_time(wl_obj, num_list, pm):
    """-----------------------------------------------------------------
        Helper function which takes a list of "words" which may or may
         not contain a valid time and attempts to interpret it.

        Arguments:
        - wl_obj -- the work log object.
        - num_list -- the source list.
        - pm -- flag indicating if the time is p.m.

        Returns:  a time object if possible, else None.
       -----------------------------------------------------------------
    """
    # Store the work log object's time_format attribute in case it needs
    #  to be reset.
    t_format = wl_obj.time_format
    # First, clean up the source list, converting all numeric strings to
    #  integers and deleting empty strings.
    s = []
    for num in num_list:
        # Screen out empty strings.
        if num:
            # Convert to integer if possible.
            s.append(wl_resource.cardinal(num))
        # end if
    # end for
    num_list = s
    # If the time words "noon" or "midnight" are anywhere in the list,
    #  replace them with their numerical equivalents.
    for n in range(len(num_list)):
        if str(num_list[n]).lower() == "noon":
            num_list[n] = 12
            pm = True
        elif str(num_list[n]).lower() == "midnight":
            num_list[n] = 0
            pm = False
        # end if
    # end for
    # If 1) there is only one element and it is a number, or 2) the
    #  first two elements are numbers, then it or they must represent
    #  the time (the rest of the string is treated as superfluous or
    #  already processed as representing am/pm).
    if (
      (len(num_list) == 1 and type(num_list[0]) == int) or
      (type(num_list[0]) == int and type(num_list[1]) == int)):
        # Make sure the hour is valid.
        hour = int(num_list[0])
        if (hour > 23) or (hour < 0):
            return None
        # If the hour can only be valid in 24-hour format, ignore the
        #  pm flag if it is set, and make sure the work log object's
        #  time_format attribute is set to 24.
        elif 12 < hour < 24:
            wl_obj.time_format = 24
        else:
            wl_obj.time_format = 12
            # If the pm flag is set, convert to 24-hour time.
            if pm and (hour < 12):
                hour += 12
            elif (not pm) and (hour == 12):
                hour = 0
            # end if
        # end if
        # If there is no second element or the second element is not
        #  a number, set the minutes to zero and discard the rest of
        #  the string.
        try:
            minute = int(num_list[1])
        # ***TODO*** try to refine this so it kicks back nonsense after
        #  the hour but accepts valid non-numerical followers.
        except (ValueError, IndexError):
            minute = 0
        # end try
        # Check the minutes.
        if (minute > 59) or (minute < 0):
            # If the time is found to be invalid at this point, make
            #  sure that any change to the time_format attribute is
            #  undone before returning.
            wl_obj.time_format = t_format
            return None
        # end if
        # Return a time object.
        return datetime.time(hour=hour, minute=minute)
    # Otherwise, non-numbers in the list must represent part or all of
    #  the time.
    # If the first element is the word "half" then the second must be an
    #  hour for the input to be valid.
    if str(num_list[0]).lower() == "half":
        minute = 30
        try:
            hour = int(num_list[1])
        except (ValueError, IndexError):
            return None
        # end try
        # Make sure the hour is valid.
        if not (0 <= hour < 24):
            return None
        if (hour > 12) or (hour == 0):
            wl_obj.time_format = 24
        elif pm:
            wl_obj.time_format = 12
            hour += 12
        # end if
        # Return a time object.
        return datetime.time(hour=hour, minute=minute)
    # end if
    # The other valid combination is number-word-number, with the word
    #  representing before or after.  First try to assign the hour and
    #  minutes.
    try:
        hour = int(num_list[2])
        minute = int(num_list[0])
    except (ValueError, IndexError):
        return None
    # end try
    # Now validate both the minutes and the hour.
    if (not (0 <= hour < 24)) or (not (0 <= minute < 60)):
        return None
    # end if
    # If the pm flag is set, adjust the hour.
    if pm and (hour < 12):
        hour += 12
    # Check the second element.  If it's before or after, set the time
    #  accordingly; otherwise just return None.
    if str(num_list[1]).lower() in ["after", "past"]:
        # For after, nothing needs adjusting.  Just return the time
        #  object.
        return datetime.time(hour=hour, minute=minute)
    if str(num_list[1]).lower() in ["before", "until", "till", "til", "to"]:
        # Note that if the user enters the extremely non-standard "zero
        # before [hour]", no adjustments need to be made.
        if minute > 0:
            # Subtract one from the hour and invert the minutes.
            hour = (hour - 1) % 24
            minute = 60 - minute
        # end if
        return datetime.time(hour=hour, minute=minute)
    # end if
    # If for some reason execution has fallen all the way through, just
    #  return None
    return None
# end function
