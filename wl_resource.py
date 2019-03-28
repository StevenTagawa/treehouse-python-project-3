"""
    Handles various resources specific to the work log object.

    Public Functions:
    - cardinal -- converts a number word into an integer.
    - format_recurrance_pattern -- takes the recurrance pattern flags
       and builds a string expressing them in plain English.
    - format_string -- converts any built-in or datetime object to a
       string.
    - month -- converts a month name to its integer equivalent.
    - numbers -- converts words or phrases representing whole numbers or
       fractions to integers or floats.
    - ordinal -- converts an ordinal day of the month (or its
       abbrevation) to its integer equivalent.
    - ordinal_string -- converts an int to an ordinal abbreviation (or,
       if between 0 and 31, the full ordinal word).  This is the inverse
       of ordinal.
    - print_header -- prints a header after the screen has been cleared.
    - print_nav -- prints a line informing the user how to go back or
       abort the current operation.
    - set_screen_width -- resets the width of the screen in characters.
    - weekday -- converts the name of a day of the week to its integer
       equivalent.

    Private Functions:
    - _normalize_date_list -- converts negative integers which represent
       days counted from the end of a month to their plain English
       equivalents.
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
    import str_utils
    import wl_datetime
    import wl_resource
except Exception as err:
    _z_exc("wl_resource.py/module imports", err)
# end try


# Constants.
DAILY = 1
WEEKLY = 2
CARD_LIST = [
  "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
  "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
  "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty",
  "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand"]
ORD_LIST = [
  "zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
  "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth",
  "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
  "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
  "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh",
  "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
MONTHS = [
  "", "January", "February", "March", "April", "May", "June", "July",
  "August", "September", "October", "November", "December"]
DAYS = [
  "", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
  "Saturday"]


def cardinal(string):
    """
        Takes a single word, and if it is a numeric string or number
         word, returns the integer that it represents.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if possible, else the original string.
       -----------------------------------------------------------------
    """
    try:
        # If the word is just the string version of a numeral, do a simple
        #  type conversion and return.  Otherwise continue.
        try:
            return int(string)
        except ValueError:
            pass
        # end try
        # See if the string is a hyphenated number.
        string_list = string.split("-")
        # Check the element(s).  If either is not a number word, return
        #  the string.
        num_list = []
        for element in string_list:
            try:
                num = CARD_LIST.index(element.lower())
                # For zero through twenty, the index position of the number
                #  word is identical to the integer value.  Use a formula to
                #  convert thirty through hundred.  For thousand, make an
                #  explicit assignment.
                if 20 < num < 29:
                    x = num - 20
                    num = 20 + (x * 10)
                elif num == 29:
                    num = 1000
                # end if
                num_list.append(num)
            except ValueError:
                return string
            # end try
        # end for
        # For compound numbers, add the elements together ONLY if the number
        #  is valid (this rejects invalid numbers joined by a hyphen, like
        #  "eleven-twelve").
        if len(num_list) == 1:
            return_int = num_list[0]
        else:
            if not (20 <= num_list[0] <= 90):
                return string
            else:
                return_int = num_list[0] + num_list[1]
            # end if
        # end if
        return return_int
    except Exception as err:
        _z_exc("wl_resource.py/cardinal", err)
    # end try
# end function


def format_recurrance_pattern(wl_obj, entry, part=False):
    """
        Parses the rec_interval attribute of a log entry object.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.

        Keyword Arguments:
        - part -- return the string as a phrase rather than a complete
           sentence (default False)

        Returns:  a string representing the entry's recurrance interval
         in plain English.
       -----------------------------------------------------------------
    """
    try:
        # The recurrance pattern is governed by five dictionary entries
        #  in the log entry object's rec_interval attribute:
        # * unit:  This is the base unit; daily, weekly, or monthly.
        # * skip:  This denotes how often to skip the base unit.  For
        #    example, if a task is flagged to recur on Tuesdays, a value
        #    of [2] for skip would change the recurrance to every other
        #    Tuesday.
        # * days:  Only relevant if unit is weekly or monthly.  Day(s)
        #    of the week for the task to recur.  Can be from [1]
        #    (Sunday) to [7] (Saturday).  This value always needs to be
        #    converted to and from Python's Monday-based week.
        # * ordinal:  Only relevant if unit is monthly and days of the
        #    week are specified; indicates on which weekdays the task
        #    should recur.  For example, if days is Tuesday, [1, 3] for
        #    ordinal indicates the first and third Tuesdays of the
        #    month.
        # * dates:  Only relevant if unit is monthly; denotes days of
        #    the month that the task should recur.  Can be from [1] to
        #    [31] for absolute dates, or [-1] to [-31] for dates
        #    relative from the end of the month; dates before the first
        #    day or after the last day of any particular month are
        #    ignored (for that month only).
        string = ""
        if not entry.rec_interval["skip"]:
            entry.rec_interval["skip"] = 1
        # end if
        if entry.rec_interval["unit"] == DAILY:
            # For daily, the only other relavant argument is skip.
            string += "Recurs every "
            if entry.rec_interval["skip"] == 2:
                string += "other "
            elif entry.rec_interval["skip"] > 2:
                string += (
                  wl_resource.ORD_LIST[entry.rec_interval["skip"]] + " ")
            # end if
            string += "day"
            if entry.rec_interval["skip"] > 1:
                string += "s"
            # end if
        elif entry.rec_interval["unit"] == WEEKLY:
            # For weekly, the relevant arguments are days and skip.
            string += "Recurs every "
            if entry.rec_interval["skip"] == 2:
                string += "other "
            elif entry.rec_interval["skip"] > 2:
                string += (
                  wl_resource.ORD_LIST[entry.rec_interval["skip"]] + " ")
            # end if
            # The default days argument is the weekday of the original
            #  task.
            if not entry.rec_interval["days"]:
                entry.rec_interval["days"] = (
                  [wl_datetime.conv_wkday(entry.date.weekday())])
            lst = []
            for day in entry.rec_interval["days"]:
                lst.append(DAYS[day])
            # end for
            string += str_utils.comma_str_from_list(lst)
        # Must be monthly.  For monthly, skip, days, dates, and ordinal
        #  may be relevant.
        else:
            string += "Recurs on the "
            if entry.rec_interval["dates"]:
                lst = _normalize_date_list(entry.rec_interval["dates"])
                string += str_utils.comma_str_from_list(lst) + " "
            elif entry.rec_interval["days"]:
                lst = []
                if entry.rec_interval["ordinal"]:
                    for o in entry.rec_interval["ordinal"]:
                        lst.append(wl_resource.ORD_LIST[o])
                    # end for
                    string += str_utils.comma_str_from_list(lst) + " "
                    lst = []
                # end if
                for day in entry.rec_interval["days"]:
                    lst.append(DAYS[day])
                # end for
                string += str_utils.comma_str_from_list(lst) + " "
            # If neither days nor dates were passed, the task recurs
            #  once a month on the date of the original task.
            else:
                entry.rec_interval["dates"] = [entry.date.day]
                string += (
                  wl_resource.ordinal_string(entry.rec_interval["dates"][0]) +
                  " ")
            # end if
            string += "of every "
            if entry.rec_interval["skip"] == 2:
                string += "other "
            elif entry.rec_interval["skip"] > 2:
                string += (
                  wl_resource.ORD_LIST[entry.rec_interval["skip"]] + " ")
            # end if
            string += "month"
        # end if
        # To make a complete sentence, add a period.
        if not part:
            string += "."
        return string
    except Exception as err:
        _z_exc("wl_resource.py/format_recurrance_pattern", err)
    # end try
# end function


def format_string(wl_obj, obj, short=False):
    """
        Formats the string representation of an object.

        Arguments:
        - wl_obj -- the work log object.
        - obj -- the object to be string-ified.

        Keyword Arguments:
        - short -- format date objects in short form (default False).

        Returns:  a string.
       -----------------------------------------------------------------
    """
    try:
        # If obj is already a string, just return it.
        if type(obj) == str:
            return obj
        # Format datetime objects by splitting them apart, calling this
        #  function recursively on each element, and then returning the
        #  combined string.
        elif type(obj) == datetime.datetime:
            return (
              format_string(wl_obj, obj.date(), short=short) + " " +
              format_string(wl_obj, obj.time(), short=short))
        # Format date and time objects using strftime.
        elif type(obj) == datetime.date:
            # Default is middle-endian
            if (not wl_obj.date_format) or (wl_obj.date_format == "M"):
                if short:
                    return obj.strftime("%m/%d/%Y")
                else:
                    return obj.strftime("%A, %B %d, %Y")
                # end if
            elif wl_obj.date_format == "L":
                if short:
                    return obj.strftime("%d/%m/%Y")
                else:
                    return obj.strftime("%A, %d %B %Y")
                # end if
            elif wl_obj.date_format == "B":
                if short:
                    return obj.strftime("%Y/%m/%d")
                else:
                    return obj.strftime("%A, %Y %B %d")
                # end if
        # Strip the leading zero from time strings, but only if it is in
        #  12-hour time.
        elif type(obj) == datetime.time:
            # Default is 12-hour time.
            if (not wl_obj.time_format) or (wl_obj.time_format == 12):
                t = obj.strftime("%I:%M %p")
                if t[0] == "0":
                    t = t[1:]
                # end if
            else:
                t = obj.strftime("%H:%M")
            # end if
        # end if
            # end if
            return t
        # Manually turn timedelta objects into hours and minutes.
        elif type(obj) == datetime.timedelta:
            d = str(obj.days)
            if d == "0":
                d = ""
                ds = ""
            elif d == "1":
                ds = " day, "
            else:
                ds = " days, "
            s = obj.seconds
            if s >= 3600:
                h = str(s // 3600)
                m = str((s % 3600) // 60)
                if h == "1":
                    hs = " hour, "
                else:
                    hs = " hours, "
                # end if
                if m == "1":
                    ms = " minute"
                else:
                    ms = " minutes"
                # end if
                return d + ds + h + hs + m + ms
            else:
                m = str(s // 60)
                if m == "1":
                    ms = " minute"
                else:
                    ms = " minutes"
                # end if
                return d + ds + m + ms
            # end if'
        # Change True and False to Yes and No.
        elif type(obj) == bool:
            if obj is True:
                return "Yes"
            else:
                return "No"
        # For all other types, just call str.
        else:
            return str(obj)
        # end if
    except Exception as err:
        _z_exc("wl_resource.py/format_string", err)
    # end try
# end function


def month(string):
    """
        Converts an integer to a month name.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    try:
        # Length check.
        if len(string) < 3:
            return None
        # end if
        string = string.title()
        for n, month in enumerate(MONTHS):
            # Search against the beginning of each month name.  Standard
            #  3-letter abbrevations will also match the correct month.
            if re.match(string, month):
                return n
            # end if
        # end for
        # If no match, return None.
        return None
    except Exception as err:
        _z_exc("wl_resource.py/month", err)
    # end try
# end function


def numbers(string):
    """-----------------------------------------------------------------
        Converts a number name/phrase to an integer or float.

        Arguments:
        - string -- the word to parse.

        Returns:  a list with number words or phrases converted to
         integers or floats.
       -----------------------------------------------------------------
    """
    try:
        # Before splitting the string, distinguish between "-" as a
        #  hyphen, and "-" as a negative sign.  Assume that negative
        #  numbers are preceded by a space (or are at the beginning of
        #  the string), and replace any negative "-"s with a flag.
        string = re.sub(r"(^-)|(\s-)", r" ~", string)
        # Divide the string into words.
        wORD_LIST = re.split(r"\s|-", string)
        # First convert all whole numbers into integers, and all
        #  fractions to floats.  Also convert "a" and "an" to 1.
        for x in range(len(wORD_LIST)):
            # If the flag is found, restore the "-".
            wORD_LIST[x] = re.sub(r"~", r"-", wORD_LIST[x])
            wORD_LIST[x] = cardinal(wORD_LIST[x])
            if re.match(r"an?$", str(wORD_LIST[x])):
                wORD_LIST[x] = 1
            elif re.match(r"\d+/\d+", str(wORD_LIST[x])):
                elements = wORD_LIST[x].split("/")
                wORD_LIST[x] = int(elements[0]) / int(elements[1])
            # end if
            den = 0
            # Look for the more common denominator words.
            if re.match(r"half", str(wORD_LIST[x])):
                den = 2
            elif re.match(r"thirds?", str(wORD_LIST[x])):
                den = 3
            elif re.match(r"(fourths?|quarters?)", str(wORD_LIST[x])):
                den = 4
            # end if
            # If a denominator was found...
            if den:
                # See if the previous word is a numerator, use it and
                #  then delete it; if it's not, set  the numerator to 1.
                if type(wORD_LIST[x - 1]) == int:
                    num = wORD_LIST[x - 1]
                    wORD_LIST[x - 1] = None
                else:
                    num = 1
                # end if
                # Calculate the float.
                wORD_LIST[x] = num / den
            # end if
        # end for
        return wORD_LIST
    except Exception as err:
        _z_exc("wl_resource.py/numbers", err)
    # end try
# end function


def ordinal(string):
    """
        Converts an ordinal word to an integer.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    try:
        # Full word.
        if string in ORD_LIST:
            return ORD_LIST.index(string)
        # end if
        try:
            return int(string[:-2])
        except ValueError:
            return None
        # end if
    except Exception as err:
        _z_exc("wl_resource.py/ordinal", err)
    # end try
# end function


def ordinal_string(number, long=False):
    """
        Convert an integer to an abbreviated ordinal.

        Arguments:
        - number -- the number to convert.

        Keyword Arguments:
        - long -- flag to return the whole word (valid only for numbers
           between 0 and 31) (default False).

        Returns:  a string representing the ordinal of the number.
       -----------------------------------------------------------------
    """
    try:
        # First make sure number is a number.
        try:
            number = int(number)
        except ValueError:
            return ""
        # end try
        # Determine abbreviation.
        if not long:
            # Identify the correct ending
            if 10 < number < 14:
                end = "th"
            else:
                if number % 10 == 1:
                    end = "st"
                elif number % 10 == 2:
                    end = "nd"
                elif number % 10 == 3:
                    end = "rd"
                else:
                    end = "th"
                # end if
            # end if
            # Return the number with the ending appended.
            return str(number) + end
        # end if
        # Otherwise, return the whole word equivalent if the number is
        #  within the valid range.
        if 0 <= number <= 31:
            return ORD_LIST[number]
        else:
            return ""
        # end if
    except Exception as err:
        _z_exc("wl_resource.py/ordinal_string", err)
    # end try
# end function


def print_header(wl_obj):
    """
        Clears the screen and prints the program header.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen.
        io_utils.clear_screen()
        # Print the header line.
        char = "-"
        for n in range(wl_obj.line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Print the title line.
        print("Work Log 1.01", end="")
        print("Steven Tagawa".rjust(wl_obj.line_length - 13))
        print("-" * wl_obj.line_length)
        print("File: ", wl_obj.filename, end="")
        if wl_obj.changed is True:
            print("   !NOT SAVED!")
        else:
            print()
        # end if
        print("Last saved:  ", end="")
        if wl_obj.last_modified:
            print(format_string(wl_obj, wl_obj.last_modified, short=True))
        else:
            print("Never")
        # end if
        print("-" * wl_obj.line_length)
        # Reset the total entries here.
        wl_obj.total_entries = len(wl_obj.entries)
        print("Total Entries: ", wl_obj.total_entries)
        # Print the footer line.
        char = "-"
        for n in range(wl_obj.line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print("\n")
        return
    except Exception as err:
        _z_exc("wl_resource.py/print_header", err)
    # end try
# end function


def print_nav(q=False, b=False):
    """
        Tells the user how to quit or go back.

        Keyword arguments:
        - q -- print quit instruction (default False).
        - b -- print back instruction (default False).

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        print()
        if b:
            print("Enter [-b] to go back.", end="")
        # end if
        if q:
            print("Enter [-q] to abort.", end="")
        # end if
        print()
        return
    except Exception as err:
        _z_exc("wl_resource.py/print_nav", err)
    # end try
# end function


def set_screen_width(wl_obj):
    """
        Resets the width of the screen in characters.

        Arguments:
        - wl_obj -- the work log object.

        Modifies:  -- the work log object's line_length attribute.

        Returns -- nothing.
       -----------------------------------------------------------------
    """
    try:
        # Display current width.
        io_utils.print_status(
          "Status",
          f"The current width of the screen is {wl_obj.line_length} " +
          "characters.",
          go=True, line_length=wl_obj.line_length)
        msg = (
          "Please enter your desired screen width (must be at least 40 " +
          "characters), or press [ENTER] to go back:")
        # Loop until user enters a valid length or quits.
        while True:
            # Get the new line length (must be >= 40).
            response = io_utils.get_input(
              msg, typ="int", line_length=wl_obj.line_length,
              must_respond=False)
            # If the user quits, leave line_length unchanged.
            if not response:
                return
            elif (response < 40):
                io_utils.print_status(
                  "Error", "You did not enter a valid number.",
                  line_length=wl_obj.line_length)
                if io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    continue
                else:
                    return
                # end if
            else:
                wl_obj.line_length = response
                return
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_resource.py/set_screen_width", err)
    # end try
# end function


def weekday(string):
    """
        Converts a day name to an integer (Sunday-based).

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    try:
        # Length check.
        if len(string) < 2:
            return None
        # end if
        # Check against weekday names.
        string = string.title()
        for n, day in enumerate(DAYS):
            # Search against the beginning of each day name.  2- and 3-
            #  letter abbreviations will also match the correct day.
            if re.match(string, day):
                return n
            # end if
        # end for
        # If no match, return None.
        return None
    except Exception as err:
        _z_exc("wl_resource.py/weekday", err)
    # end try
# end function


def _normalize_date_list(d_list):
    """
        Converts a list of date integers to ordinals.

        Arguments:
        - d_list -- the list of integers to convert.

        Returns:  a list of ordinal numbers or phrases.
       -----------------------------------------------------------------
    """
    try:
        ORD_LIST = []
        rel_list = []
        for date in d_list:
            # This should never happen...
            if date == 0:
                return []
            # Separate out the positive numbers; convert to ordinals.
            elif date > 0:
                ORD_LIST.append(wl_resource.ordinal_string(date))
            # Convert the negative numbers to their word equivalents.
            else:
                if date == -1:
                    rel_list.append("last day")
                elif date == -2:
                    rel_list.append("next to the last day")
                else:
                    rel_list.append(
                      wl_resource.ordinal_string(abs(date)) +
                      " to the last day")
                # end if
            # end if
        # end for
        # Return the two lists, joined together; ordinals first,
        #  relative dates after.  Note that the list is not guaranteed
        #  to be in numerical order, but it doesn't need to be for this
        #  purpose.
        return ORD_LIST + rel_list
    except Exception as err:
        _z_exc("wl_resource.py/normalize_date_list", err)
    # end try
# end function
