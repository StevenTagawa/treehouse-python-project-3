# Imports.
import datetime
import re

import io_utils
import str_utils
import wl_datetime
import wl_resource


# Constants.
DAILY = 1
WEEKLY = 2


"""---------------------------------------------------------------------
    Handles various resources for the work log.
   ---------------------------------------------------------------------
"""

card_list = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
    "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
    "thousand"]

ord_list = [
    "zeroth", "first", "second", "third", "fourth", "fifth", "sixth",
    "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth",
    "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
    "eighteenth", "nineteenth", "twentieth", "twenty-first",
    "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth",
    "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth",
    "thirtieth", "thirty-first"]

months = [
    "", "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"]

days = [
    "", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday"]


def cardinal(string):
    """-----------------------------------------------------------------
        Takes a single word, and if it is a numeric string or number
         word, returns the integer that it represents.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if possible, else the original string.
       -----------------------------------------------------------------
    """
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
            num = card_list.index(element.lower())
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
# end function


def format_recurrance_pattern(wl_obj, entry, part=False):
    """-----------------------------------------------------------------
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
    # The recurrance pattern is governed by five dictionary entries in
    #  the log entry object's rec_interval attribute:
    # * unit:  This is the base unit; daily, weekly, or monthly.
    # * skip:  This denotes how often to skip the base unit.  For
    #    example, if a task is flagged to recur on Tuesdays, a value of
    #    2 for skip would change the recurrance to every other Tuesday.
    # * days:  Only relevant if unit is weekly or monthly.  Day(s) of
    #    the week for the task to recur.  Can be from 1 (Sunday) to 7
    #    (Saturday).  This value always needs to be converted to and
    #    from Python's Monday-based week.
    # * ordinal:  Only relevant if unit is monthly and days of the week
    #    are specified; indicates on which weekdays the task should
    #    recur.  For example, if days is Tuesday, [1, 3] for ord
    #    indicates the first and third Tuesdays of the month.
    # * dates:  Only relevant if unit is monthly; denotes days of the
    #    month that the task should recur.  Can be from 1 to 31; dates
    #    beyond the last day of any particular month are ignored (for
    #    that month only).
    string = ""
    if not entry.rec_interval["skip"]:
        entry.rec_interval["skip"] = 1
    # end if
    if entry.rec_interval["unit"] == DAILY:
        # For daily, the only other argument that is relevant is skip.
        string += "Recurs every "
        if entry.rec_interval["skip"] == 2:
            string += "other "
        elif entry.rec_interval["skip"] > 2:
            string += wl_resource.ord_list[entry.rec_interval["skip"]] + " "
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
            string += wl_resource.ord_list[entry.rec_interval["skip"]] + " "
        # end if
        # The default days argument is the weekday of the original task.
        if not entry.rec_interval["days"]:
            entry.rec_interval["days"] = (
              [wl_datetime.conv_wkday(entry.date.weekday())])
        l = []
        for day in entry.rec_interval["days"]:
            l.append(wl_resource.days[day])
        # end for
        string += str_utils.comma_str_from_list(l)
    # Must be monthly.  For monthly, skip, days, dates, and ordinal may
    #  be relevant.
    else:
        string += "Recurs on the "
        if entry.rec_interval["dates"]:
            l = _normalize_date_list(entry.rec_interval["dates"])
            string += str_utils.comma_str_from_list(l) + " "
        elif entry.rec_interval["days"]:
            l = []
            if entry.rec_interval["ordinal"]:
                for o in entry.rec_interval["ordinal"]:
                    l.append(wl_resource.ord_list[o])
                # end for
                string += str_utils.comma_str_from_list(l) + " "
                l = []
            # end if
            for day in entry.rec_interval["days"]:
                l.append(wl_resource.days[day])
            # end for
            string += str_utils.comma_str_from_list(l) + " "
        # If neither days nor dates were passed, the task recurs once a
        #  month on the date of the original task.
        else:
            entry.rec_interval["dates"] = [entry.date.day]
            string += (
              wl_resource.ordinal_string(entry.rec_interval["dates"][0]) + " ")
        # end if
        string += "of every "
        if entry.rec_interval["skip"] == 2:
            string += "other "
        elif entry.rec_interval["skip"] > 2:
            string += wl_resource.ord_list[entry.rec_interval["skip"]] + " "
        # end if
        string += "month"
    # end if
    # To make a complete sentence, add a period.
    if not part:
        string += "."
    return string
# end function


def format_string(wl_obj, obj, short=False):
    """-------------------------------------------------------------
        Takes an object representable by a string and returns a
         formatted string.

        Arguments:
        - wl_obj -- the work log object.
        - obj -- the object to be string-ified.

        Keyword Arguments:
        - short -- format date objects in short form (default False).

        Returns:  a string.
       -------------------------------------------------------------
    """
    # If obj is already a string, just return it.
    if type(obj) == str:
        return obj
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
            #end if
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
        if obj == True:
            return "Yes"
        else:
            return "No"
    # For all other types, just call str.
    else:
        return str(obj)
    # end if
# end function


def month(string):
    """-----------------------------------------------------------------
        Takes a word, checks to see if it is the name of a month, and
         if it is, returns an integer (January = 1, December = 12)
         representing that month.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    # Length check.
    if len(string) < 3:
        return None
    # end if
    string = string.title()
    for n, month in enumerate(months):
        # Search against the beginning of each month name.  Standard 3-
        #  letter abbrevations will also match the correct month.
        if re.match(string, month):
            return n
        # end if
    # end for
    # If no match, return None.
    return None
# end function


def numbers(string):
    """-----------------------------------------------------------------
        Takes a string, looks through it for any number or word
         combinations that represent whole numbers or fractions and
         converts them to integers or floats.

        Arguments:
        - string -- the word to parse.

        Returns:  a list with number words or phrases converted to
         integers or floats.
       -----------------------------------------------------------------
    """
    # Divide the string into words.
    word_list = re.split("\s|-", string)
    # First convert all whole numbers into integers, and all fractions
    #  to floats.  Also convert "a" and "an" to 1.
    for x in range(len(word_list)):
        word_list[x] = cardinal(word_list[x])
        if re.match(r"an?$", str(word_list[x])):
            word_list[x] = 1
        elif re.match(r"\d+/\d+", str(word_list[x])):
            elements = word_list[x].split("/")
            word_list[x] = int(elements[0]) / int(elements[1])
        # end if
        den = 0
        # Look for the more common denominator words.
        if re.match(r"half", str(word_list[x])):
            den = 2
        elif re.match(r"thirds?", str(word_list[x])):
            den = 3
        elif re.match(r"(fourths?|quarters?)", str(word_list[x])):
            den = 4
        # end if
        # If a denominator was found...
        if den:
            # See if the previous word is a numerator, use it and then
            #  delete it; if it's not, set  the numerator to 1.
            if type(word_list[x - 1]) == int:
                num = word_list[x - 1]
                word_list[x - 1] = None
            else:
                num = 1
            # end if
            # Calculate the float.
            word_list[x] = num / den
        # end if
    # end for
    return word_list
# end function


def ordinal(string):
    """-----------------------------------------------------------------
        Takes a word, checks to see if it the name of an ordinal day of
         of the month, and if it is, returns an integer corresponding to
         the day.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    # Full word.
    if string in ord_list:
        return ord_list.index(string)
    # end if
    try:
        return int(string[:-2])
    except ValueError:
        return None
    # end if
# end function


def ordinal_string(number):
    """-----------------------------------------------------------------
        Takes an integer and returns its abbreviated ordinal form.

        Arguments:
        - number -- the number to convert.

        Returns:  a string representing the ordinal of the number.
       -----------------------------------------------------------------
    """
    # First make sure number is a number.
    try:
        number = int(number)
    except ValueError:
        return ""
    # end try
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
# end function


def print_header(wl_obj):
    """-----------------------------------------------------------------
        Clears the screen and then prints the program header at the top.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    # Clear the screen.
    io_utils.clear_screen()
    # Print the header
    print(
      "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(
      "Work Log 1.0                                            Steven Tagawa")
    print("-" * 69)
    print("File: ", wl_obj.filename, end="")
    if wl_obj.changed == True:
        print("   !NOT SAVED!")
    else:
        print()
    # end if
    print("-" * 69)
    # Reset the total entries here.
    wl_obj.total_entries = len(wl_obj.entries)
    print("Total Entries: ", wl_obj.total_entries)
    print(
      "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print()
    return
# end function


def print_nav(q=False, b=False):
    """-----------------------------------------------------------------
        Tells the user how to quit or go back.

        Keyword arguments:
        - q -- print quit instruction (default False).
        - b -- print back instruction (default False).

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    print()
    if b:
        print("Enter [-b] to go back.", end="")
    # end if
    if q:
        print("Enter [-q] to abort.", end="")
    # end if
    print()
    return
# end function


def print_status(msg_type, msg="", go=False):
    """-----------------------------------------------------------------
        Prints a status or error message, optionally waits for the user
         to press [ENTER] to continue.

        Arguments:
        - msg_type -- the type of status to print.

        Keyword Arguments:
        - msg -- the message to print
        - go -- return without waiting for the user (default False).

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    # Print the header line.
    if msg_type == "status":
        print(
          "\n-=-=-{Status}=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
    elif msg_type == "error":
        print(
          "\n-=-=-{Error}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
    elif msg_type == "warning":
        print(
          "\n-=-=-{Warning}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
    else:
        print(
          "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
    # end if
    print(msg)
    print(
      "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    # Optionally wait for the user.
    if not go:
        input("Press [ENTER] to continue.")
    # end if
    return
# end function


def weekday(string):
    """-----------------------------------------------------------------
        Takes a word, checks to see if it is the name of a day of the
         week, and if it is, returns an integer (Sunday = 1, Saturday =
         7) representing that day.

        Arguments:
        - string -- the word to parse.

        Returns:  an integer if successful; otherwise None.
       -----------------------------------------------------------------
    """
    # Length check.
    if len(string) < 2:
        return None
    # end if
    # Check against weekday names.
    string = string.title()
    for n, day in enumerate(days):
        # Search against the beginning of each day name.  2- and 3-
        #  letter abbreviations will also match the correct day.
        if re.match(string, day):
            return n
        # end if
    # end for
    # If no match, return None.
    return None
# end function


def _normalize_date_list(d_list):
    """-----------------------------------------------------------------
        Takes a list of integers representing dates, both absolute and
         relative, and converts them into plain-English equivalents.

        Arguments:
        - d_list -- the list of integers to convert.

        Returns:  a list of ordinal numbers or phrases.
       -----------------------------------------------------------------
    """
    ord_list = []
    rel_list = []
    for date in d_list:
        # This should never happen...
        if date == 0:
            return []
        # Separate out the positive numbers; convert to ordinals.
        elif date > 0:
            ord_list.append(wl_resource.ordinal_string(date))
        # Convert the negative numbers to their word equivalents.
        else:
            if date == -1:
                rel_list.append("last day")
            elif date == -2:
                rel_list.append("next to the last day")
            else:
                rel_list.append(
                  wl_resource.ordinal_string(abs(date) - 1) +
                  "to the last day")
            # end if
        # end if
    # end for
    # Return the two lists, joined together; ordinals first, relative
    #  dates after.  Note that the list is not guaranteed to be in
    #  objective order, but it doesn't need to be for this purpose.
    return ord_list + rel_list
# end function
