"""
    Contains date- and time-related functions.

    Public Functions:
    - calc_duration_abs -- converts the user's input of a duration to
       a timedelta object.
    - calc_duration_rel -- calculates a duration given a task's start
       time and the user's input of an end time, and converts it to a
       timedelta object.
    - conv_wkday -- converts an integer representing a day of the week
       from Python's Monday-based week to a Sunday-based week.
    - dformat -- converts a date object to a string based on the user's
       preferred date format.
    - find_weekday -- determines the day of the month on which a
       specified day of the week falls.
    - last_date -- determines the last date of a month.
    - parse_date_calendar -- parses a list of 2 or 3 elements to see if
       it contains a valid date with the month or day written out.
    - parse_date_input -- the primary date parser; takes the user's
       input of a date, in any format, and runs it through various
       parsing functions to try to interpret it.
    - parse_date_numeric -- parses the user's input to see if it is a
       valid date in a numeric format; if it is, creates a time object.
    - parse_date_phrase -- parses the user's input to see if it is a
       word or phrase that represents a valid date; if it is, creates a
       date object.
    - parse_duration_input -- the main duration parser; takes the user's
       input of a duration or an end time and runs it through various
       parsing functions to try to interpret it.
    - parse_time_input -- the main time parser; takes the user's input
       of a time, in any format, and formats it so that it can be
       validated.
    - set_endian -- sets or resets the user's preferred date format.
    - set_time_format -- sets or resets the user's preferred time
       format.

    Private Functions:
    - _check_calendar_date -- checks a set of 2 or 3 elements to see if
       they form a valid date in the user's preferred date format.
    - _check_other_endians -- checks a list of 3 numbers to see if they
       form a valid date in a date format other than the one selected.
    - _create_date -- attempts to create a date object from 3 numbers.
    - _create_date_from_weekday -- creates a date object given a
       specified day of the week.
    - _create_time -- takes the user's input of a time and attempts to
       create a time object from it.
    - _z_exc -- generic exception handler.
   ---------------------------------------------------------------------
"""


# Import sys.
import sys


def _z_exc(loc, err):
    """
        Catch-all exception handler.

        Arguments:
        - loc -- string naming the module/function/method in which the
           exception occurred.
        - err -- the exception string.

        Returns:  nothing (exits program).
       -----------------------------------------------------------------
    """
    # Print error information.
    print("An interal error occurred in " + loc + ": ", err)
    # Exit.
    sys.exit(
      "Please report the above error and the circumstances which caused it " +
      "to the developer.")
    return  # Superfluous return.
# end function


# Other imports.
try:
    import datetime
    import re

    import io_utils
    import wl_resource
except Exception as err:
    _z_exc("wl_datetime.py/module imports", err)
# end try


def calc_duration_abs(wl_obj, string):
    """
        Parses a string and determines the duration it describes.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the string to parse.

        Returns:  a timedelta object if a valid duration is found; else
         None.
       -----------------------------------------------------------------
    """
    try:
        # If the string is "max", return the maximum timedelta.
        if string.lower() == "max":
            return datetime.timedelta.max
        # end if
        # Otherwise the string must contain one or more number/word
        #  pairs:  a number (or number phrase) and a unit of measure.
        #  These should (but need not be) in descending order.
        #
        # First, convert any numbers.
        raw_list = wl_resource.numbers(string)
        # Then cull unneeded elements from the list.
        word_list = []
        for word in raw_list:
            if not ((word is None) or (str(word).lower() == "and")):
                word_list.append(word)
            # end if
        # end for
        # Now move through the string from left to right.
        minutes = None
        hours = None
        days = None
        ndx = 0
        while ndx < len(word_list):
            amt = None
            # An inner loop adds numbers together.  If there aren't any,
            #  amt will remain None.  (The function must differentiate
            #  here between None and 0.)
            while (
              (ndx < len(word_list) and type(word_list[ndx]) in [int, float])):
                if amt is None:
                    amt = word_list[ndx]
                else:
                    amt += word_list[ndx]
                # end if
                ndx += 1
            # end while
            # If there was no amount, check for an unspaced number/unit
            #  combination.
            if amt is None:
                if re.match(r"\d+m[inutes]?", word_list[ndx]):
                    minutes = int(re.match(r"\d+", word_list[ndx]).group())
                    ndx += 1
                    continue
                if re.match(r"\d+h[ours]?", word_list[ndx]):
                    hours = int(re.match(r"\d+", word_list[ndx]).group())
                    ndx += 1
                    continue
                if re.match(r"\d+d[ays]?", word_list[ndx]):
                    days = int(re.match(r"\d+", word_list[ndx]).group())
                    ndx += 1
                    continue
                # Otherwise just move to the next word.
                ndx += 1
                continue
            # end if
            # Determine the units (if not valid, just move to the next
            #  word).  But don't do this if the previous word was the
            #  last.
            if ndx < len(word_list):
                if re.match(r"m\w*", word_list[ndx]):
                    minutes = amt
                elif re.match(r"h\w*", word_list[ndx]):
                    hours = amt
                elif re.match(r"d\w*?", word_list[ndx]):
                    days = amt
                # end if
                ndx += 1
            # end if
        # end while
        # Having gone through the list, see if any times were found.  If
        #  not, return None.
        if (minutes is None) and (hours is None) and (days is None):
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
        # Create a timedelta created from the times found.  Note that
        #  zero minutes is a valid duration, but negative durations are
        #  not valid.
        td = datetime.timedelta(days=days, hours=hours, minutes=minutes)
        # Check if the timedelta is negative.  If it is, print an error
        #  and return None.
        if td < datetime.timedelta():
            io_utils.print_status(
              "Error", "The duration cannot be negative.",
              line_length=wl_obj.line_length)
            return None
        # end if
        return td
    except Exception as err:
        _z_exc("wl_datetime/calc_duration_abs", err)
    # end try
# end function


def calc_duration_rel(wl_obj, end_time, start_time):
    """
        Determines a duration based on two times.

        Arguments:
        - wl_obj -- the work log object.
        - end_time -- the ending time.
        - start_time -- the starting time.

        Returns:  a timedelta object representing the difference between
         the two times, if that difference is positive; else None.
       -----------------------------------------------------------------
    """
    try:
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
            io_utils.print_status("Error", msg, line_length=wl_obj.line_length)
            return None
        # end if
    except Exception as err:
        _z_exc("wl_datetime/calc_duration_rel", err)
    # end try
# end function


def conv_wkday(day, iso=False):
    """
        Converts from Monday-based weekday to Sunday-based.

        Arguments:
        - day -- the weekday to convert.

        Keyword Arguments:
        - iso -- Set if the isoweekday method was used (default False).

        Returns:  an integer between 1 (Sunday) and 7 (Saturday).
       -----------------------------------------------------------------
    """
    try:
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
    except Exception as err:
        _z_exc("wl_datetime/conv_wkday", err)
    # end try
# end function


def dformat(date, endian):
    """
        Takes a date and formats it accoring to the correct endian.

        Arguments:
        - date -- the date object to convert.
        - endian -- the work log object's endian attribute.

        Returns:  a string representing the date.
       -----------------------------------------------------------------
    """
    try:
        # Return a string in the proper format.
        if endian == "B":
            return date.strftime("%Y/%m/%d")
        elif endian == "M":
            return date.strftime("%m/%d/%Y")
        else:
            return date.strftime("%d/%m/%Y")
        # end if
    except Exception as err:
        _z_exc("wl_datetime/dformat", err)
    # end try
# end function


def find_weekday(day, ordinal, month, year):
    """
        Determines the date on which a specific day of the week falls.

        Keyword Arguments:
        - day -- the day of the week to find.
        - ordinal -- which week to find.
        - month -- the month in which to search.
        - year -- the year in which to search.

        Returns:  a date object representing the correct day, or None if
         the specified day does not occur within the specified month.
       -----------------------------------------------------------------
    """
    try:
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
    except Exception as err:
        _z_exc("wl_datetime/find_weekday", err)
    # end try
# end function


def last_date(month, year):
    """
        Returns the last date of a given month.

        Arguments:
        - month -- the month to check.
        - year -- the year to check.

        Returns:  an integer between 28 and 31, representing the last
         date of the specified month.
       -----------------------------------------------------------------
    """
    try:
        # Standard months.
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        # February.
        else:  # month == 2
            # Rather than re-creating a complex formula, just try to
            #  create a date object for Febuary 29 and see if it works.
            try:
                datetime.date(year, month, 29)
                return 29
            except ValueError:
                return 28
            # end try
        # end if
    except Exception as err:
        _z_exc("last_date", err)
    # end try
# end function


def parse_date_calendar(wl_obj, word_list):
    """
        Parses a word list for a date.

        Sees if the list contains a date with either the month or day
         spelled out.

        Arguments:
        - wl_obj -- the work log object.
        - word_list -- the list of words to parse.

        Returns:  a date object if successful; else None.
       -----------------------------------------------------------------
    """
    try:
        # Check all the elements in every order.  If one matches, set
        #  the work log object's date_format attribute and return the
        #  date object.
        if len(word_list) == 2:
            # Month and day.  Note--don't set the date format here,
            #  becuase it could be either big-endian or middle-endian.
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
    except Exception as err:
        _z_exc("wl_datetime/parse_date_calendar", err)
    # end try
# end function


def parse_date_input(wl_obj, string):
    """
        Extracts a date from user input.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, else None.
       -----------------------------------------------------------------
    """
    try:
        # If the string is a standard numeric date, check to make sure
        #  it is valid.  The result will either be a date object or
        #  None.
        if re.search(r"^\d{1,4}[-/.]{1}\d{1,4}[-/.]?\d{1,4}$", string):
            return parse_date_numeric(wl_obj, string)
        # Otherwise check to see if it is a valid word date.  The result
        #  will still be a date object or None.
        else:
            return parse_date_phrase(wl_obj, string)
        # end if
    except Exception as err:
        _z_exc("wl_datetime/parse_date_input", err)
    # end try
# end function


def parse_date_numeric(wl_obj, string):
    """
        Validates a numeric date in the current format.

        Allows the date format to be changed if the numeric combination
         is a valid date in a different format.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    try:
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
        # If there are only two elements, the year was omitted and
        #  defaults to the current year.  Where the year element is
        #  inserted depends on the format.
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
            io_utils.print_status(
              "Error", f"{string} could not be interpreted as a valid date.",
              line_length=wl_obj.line_length)
            return None
        # end if
        # Otherwise, inform the user of the successful format(s) and ask
        #  if he/she wants to change the selected format to match, or
        #  re-enter the date.
        msg = io_utils.print_block(
          f"The date {string} is not valid in the currently selected " +
          "format, but is valid in a different format.  You can choose to " +
          "change the date format or re-enter the date for this task.",
          str_=True)
        io_utils.print_status("Warning", msg, line_length=wl_obj.line_length)
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
        response = io_utils.menu(option_list, keystroke_list="#", quit_=False)
        # If the user chose to try again, return None.
        if response == len(option_list):
            input("Press [ENTER] to continue.")
            return None
        # Otherwise, reset the date format and return the date object.
        else:
            wl_obj.date_format = valid_formats[response - 1]
            return valid_dates[response - 1]
        # end if
    except Exception as err:
        _z_exc("wl_datetime/parse_date_numeric", err)
    # end try
# end function


def parse_date_phrase(wl_obj, string):
    """
        Function that checks a string to see if it contains a valid word
         date.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    try:
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
            # There are three valid one-word responses, plus the days of
            #  the week.
            if word_list[0].lower() == "today":
                return datetime.date.today()
            elif word_list[0].lower() == "yesterday":
                return datetime.date.today() - datetime.timedelta(days=1)
            elif word_list[0].lower() == "tomorrow":
                return datetime.date.today() + datetime.timedelta(days=1)
            else:
                valid = wl_resource.weekday(word_list[0])
                # If the string is a day of the week, return the date
                #  object that corresponds to that day of the current
                #  week.  Else return None.
                if valid:
                    return _create_date_from_weekday(valid, 0)
                else:
                    io_utils.print_status(
                      "Error",
                      f"{string} could not be interpreted as a valid date.",
                      line_length=wl_obj.line_length)
                    return None
                # end if
            # end if
        elif len(word_list) == 2:
            # A two-word response can be a calendar date without the
            #  year, or a phrase.  Check for a calendar date first.
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
                io_utils.print_status(
                  "Error",
                  f"{string} could not be interpreted as a valid date.",
                  line_length=wl_obj.line_length)
                return None
            # end if
            valid = wl_resource.weekday(word_list[1])
            if valid:
                return _create_date_from_weekday(valid, offset)
            else:
                io_utils.print_status(
                  "Error",
                  f"{string} could not be interpreted as a valid date.",
                  line_length=wl_obj.line_length)
                return None
            # end if
        elif len(word_list) == 3:
            # Three word calendar dates are a full month, day and year
            #  (but not necessarily in that order).  Check for them.
            good = parse_date_calendar(wl_obj, word_list)
            if good:
                return good
            # end if
            # There are two set three-word date phrases.  It's simpler
            #  to search for them in the original string.
            if re.search(r"day after tomorrow", string, re.I):
                return datetime.date.today() + datetime.timedelta(days=2)
            elif re.search(r"day before yesterday", string, re.I):
                return datetime.date.today() - datetime.timedelta(days=2)
            # end if
            # Other three-word date phrases are a day of the week
            #  followed by either "before last" or "after next".
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
                    io_utils.print_status(
                      "Error",
                      f"{string} could not be interpreted as a valid date.",
                      line_length=wl_obj.line_length)
                    return None
                # end if
            else:
                io_utils.print_status(
                  "Error",
                  f"{string} could not be interpreted as a valid date.",
                  line_length=wl_obj.line_length)
                return None
            # end if
        else:
            io_utils.print_status(
              "Error", f"{string} could not be interpreted as a valid date.",
              line_length=wl_obj.line_length)
            return None
        # end if
    except Exception as err:
        _z_exc("wl_datetime/parse_date_phrase", err)
    # end try
# end function


def parse_duration_input(wl_obj, entry, string):
    """
        Extracts a duration from user input.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.
        - string -- the user input.

        Returns:  a timedelta object if successful, or None.
       -----------------------------------------------------------------
    """
    try:
        # First just check to see if it's a end time.
        end_time = parse_time_input(wl_obj, string)
        # If it is a time, send to the function to calculate the
        #  duration.
        if end_time:
            return calc_duration_rel(wl_obj, end_time, entry.time)
        # end if
        # Otherwise, send to the function to construct the duration from
        #  the string.
        return calc_duration_abs(wl_obj, string)
    except Exception as err:
        _z_exc("wl_datetime/parse_duration_input", err)
    # end try
# end function


def parse_time_input(wl_obj, string):
    """
        Extracts a time from user input.

        Arguments:
        - wl_obj -- the work log object.
        - string -- the user input.

        Returns:  a time object if successful, or None.
       -----------------------------------------------------------------
    """
    try:
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
        # If the string is all numbers (with or without a colon) it can
        #  be processed directly.
        if re.match(r"\d{1,2}:?\d{0,2}\s?(a[.]?m?[.]?|p[.]?m?[.]?)?$", string):
            num_list = re.split(r"\D", string)
            # if the first number is 3-4 digits, it can only be a
            #  complete time.  If it is 1-2 digits, it must be an hour,
            #  and minutes may follow.
            #
            # If a valid time in 24-hour format is entered, the pm flag
            #  is ignored and the time_format attribute reset to 24.
            #
            # Ambiguous times in 12-hour format are assumed to be AM
            #  unless the pm flag is set.
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
                # Add to the final word list either the word or its
                #  integer equivalent.
                word_list.append(wl_resource.cardinal(element))
            # end for
        # end for
        # With all numeric strings and number words converted to
        #  integers, return either a time object or None.
        return _create_time(wl_obj, word_list, pm)
    except Exception as err:
        _z_exc("wl_datetime/parse_time_input", err)
    # end try
# end function


def set_endian(wl_obj):
    """
        Allows the user to set the preferred date format.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  nothing
       -----------------------------------------------------------------
    """
    try:
        # Endian examples.
        end_list = [
          "July 15, 2010 (7/15/10)", "15 July, 2010 (15/7/10)",
          "2010 July 15 (10/7/15)"]
        # Print explanation.
        if wl_obj.date_format:
            msg = "The current date format is "
            if wl_obj.date_format == "M":
                msg += end_list[0]
            elif wl_obj.date_format == "L":
                msg += end_list[1]
            else:  # wl_obj.date_format == "B"
                msg += end_list[2]
            # end if
        else:
            msg = "The date format has not been set."
        # end if
        io_utils.print_status(
          "Status", msg, go=True, line_length=wl_obj.line_length)
        # If a date format is already set, allow the user to leave it.
        if wl_obj.date_format:
            q = True
        else:
            q = False
        # end if
        # Ask the user to set a date format.
        response = io_utils.menu(
          end_list, keystroke_list="#", confirm=True, quit_=q,
          prompt="Please select your preferred date format:")
        if response == 0:
            return
        elif response == 1:
            wl_obj.date_format = "M"
        elif response == 2:
            wl_obj.date_format = "L"
        else:  # response == 3
            wl_obj.date_format = "B"
        # end if
        return
    except Exception as err:
        _z_exc("wl_datetime/set_endian", err)
    # end try
# end function


def set_time_format(wl_obj):
    """
        Allows the user to set the preferred time format.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  nothing
       -----------------------------------------------------------------
    """
    try:
        # Build message.
        if not wl_obj.time_format:
            msg = "The time format has not been set."
        elif wl_obj.time_format == 12:
            msg = "The current time format is 12-hour (AM/PM)."
        else:  # wl_obj.time_format == 24
            msg = "The current time format is 24-hour (Military Time)."
        # end if
        # Print status.
        io_utils.print_status(
          "Status", msg, go=True, line_length=wl_obj.line_length)
        # Display menu and get response.
        response = io_utils.menu(
          ["12-hour Clock (AM/PM)", "24-hour Clock (Military Time)"],
          keystroke_list="#")
        # If the user chose to quit, just return without changing
        #  anything.
        if response == 0:
            return
        # Else set the time_format attribute to the user's choice.
        elif response == 1:
            wl_obj.time_format = 12
        else:  # response == 2
            wl_obj.time_format = 24
        # end if
        return
    except Exception as err:
        _z_exc("wl_datetime/set_time_format", err)
    # end try
# end function


def _check_calendar_date(month, day, year=None):
    """
        Checks two or three words to see if they form a valid date.

        Arguments:
        - month -- the word representing the month.
        - day -- the word representing the day.

        Keyword Arguments:
        - year -- the word representing the year.

        Returns:  a date object if successful; else None.
       -----------------------------------------------------------------
    """
    try:
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
    except Exception as err:
        _z_exc("wl_datetime/_check_calendar_date", err)
    # end try
# end function


def _check_other_endians(numbers, endian):
    """
        Validates a date in formats NOT currently preferred.

        Arguments:
        - numbers -- the numbers that form the potential date.
        - endian -- the date format to NOT test.

        Returns:  a list of zero to two characters indicating for which
         formats the numbers form a valid date (if any), and a list of
         corresponding date objects.
       -----------------------------------------------------------------
    """
    try:
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
    except Exception as err:
        _z_exc("wl_datetime/_check_other_endians", err)
    # end try
# end function


def _create_date(numbers, endian):
    """
        Creates a date from a set of numbers.

        Arguments:
        - numbers -- the numbers that form the potential date.
        - endian -- the date format.

        Returns:  a date object if successful, or None.
       -----------------------------------------------------------------
    """
    try:
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
        #  abbreviated years.  4-digit years can be between 1900 and
        #  2099.)
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
    except Exception as err:
        _z_exc("wl_datetime/_create_date", err)
    # end try
# end function


def _create_date_from_weekday(weekday, offset):
    """
        Creates a date given a day of the week.

        Arguments:
        - weekday -- the day of the week for which to create the date.
        - offset -- the week in which to create the date.

        Returns:  a date object.
       -----------------------------------------------------------------
    """
    try:
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
          datetime.date.today() + datetime.timedelta(days=day_offset) +
          datetime.timedelta(days=week_offset))
    except Exception as err:
        _z_exc("wl_datetime/_create_date_from_weekday", err)
    # end try
# end function


def _create_time(wl_obj, num_list, pm):
    """
        Creates a time from a list of words.

        Arguments:
        - wl_obj -- the work log object.
        - num_list -- the source list.
        - pm -- flag indicating if the time is p.m.

        Returns:  a time object if possible, else None.
       -----------------------------------------------------------------
    """
    try:
        # Store the work log object's time_format attribute in case it
        #  needs to be reset.
        t_format = wl_obj.time_format
        # First, clean up the source list, converting all numeric
        #  strings to integers and deleting empty strings.
        s = []
        for num in num_list:
            # Screen out empty strings.
            if num:
                # Convert to integer if possible.
                s.append(wl_resource.cardinal(num))
            # end if
        # end for
        num_list = s
        # If the time words "noon" or "midnight" are anywhere in the
        #  list, replace them with their numerical equivalents.
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
        #  first two elements are numbers, then it or they must
        #  represent the time (the rest of the string is treated as
        #  superfluous or already processed as representing am/pm).
        if (
          (len(num_list) == 1 and type(num_list[0]) == int) or
          (type(num_list[0]) == int and type(num_list[1]) == int)):
            # Make sure the hour is valid.
            hour = int(num_list[0])
            if (hour > 23) or (hour < 0):
                return None
            # If the hour can only be valid in 24-hour format, ignore
            #  the pm flag if it is set, and make sure the work log
            #  object's time_format attribute is set to 24.
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
            # TODO:  try to refine this so it kicks back nonsense after
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
        # Otherwise, non-numbers in the list must represent part or all
        #  of the time.
        # If the first element is the word "half" then the second must
        #  be an hour for the input to be valid.
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
        # The other valid combination is number-word-number, with the
        #  word representing before or after.  First try to assign the
        #  hour and minutes.
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
        # Check the second element.  If it's before or after, set the
        #  time accordingly; otherwise just return None.
        if str(num_list[1]).lower() in ["after", "past"]:
            # For after, nothing needs adjusting.  Just return the time
            #  object.
            return datetime.time(hour=hour, minute=minute)
        if str(num_list[1]).lower() in [
          "before", "until", "till", "til", "to"]:
            # Note that if the user enters the extremely non-standard
            #  "zero before [hour]", no adjustments need to be made.
            if minute > 0:
                # Subtract one from the hour and invert the minutes.
                hour = (hour - 1) % 24
                minute = 60 - minute
            # end if
            return datetime.time(hour=hour, minute=minute)
        # end if
        # If for some reason execution has fallen all the way through,
        #  just return None
        return None
    except Exception as err:
        _z_exc("wl_datetime/_create_time", err)
    # end try
# end function
