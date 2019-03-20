"""---------------------------------------------------------------------
    Contains generic string-related functions.

    Public Functions:
    - comma_str_from_list -- converts a list into a string, with commas
       and the word "and" properly inserted.
    - str_to_container -- converts a string that represents a list,
       tuple or dictionary to the appropriate type.
    - str_to_num -- converts a string representing a number to an int,
       float or complex number.
    - str_to_bool - converts a string representing True or False (or yes
       or no) to a bool.
    - str_to_datetime - converts a string representing a date, time,
       datetime, or timedelta object to the appropriate object.

    Private Methods:
    - _date_fromisoformat -- converts a formatted string to a date
       object; replicates the fromisoformat method for environments
       below Python 3.7.
    - _datetime_fromisoformat -- converts a formatted string to a
       datetime object; replicates the fromisoformat method for
       environments below Python 3.7.
    - _time_fromisoformat -- converts a formatted string to a time
       object; replicates the fromisoformat method for environments
       below Python 3.7.
    - _z_exc -- generic exception handler.
   ---------------------------------------------------------------------
"""


# Imports.
import re
import datetime


def comma_str_from_list(lst):
    """-----------------------------------------------------------------
        Takes a list or other string-convertible iterable and returns
        a comma-delinated string.

        Arguments:
        - lst -- the list or iterable to process.

        Returns:  a string with the iterable's elements separated by
         commas and an "and".
       -----------------------------------------------------------------
    """
    string = ""
    for n, element in enumerate(lst):
        # First make sure the element is in string form.
        element = str(element)
        string += element
        if n == len(lst) - 2:
            string += " and "
        elif n < len(lst) - 2:
            string += ", "
        # end if
    # end for
    return string
# end function


def str_to_container(string):
    """-----------------------------------------------------------------
        Takes a string representation of a list, tuple or dictionary and
         converts it back to that type.  Converts in place any nested
         containers within the main container.  Converts any string
         representation of a numeric or boolean value, within
         any container, to the correct type.

        Arguments:
        - string -- the string to convert.

        Returns:  a list, or the original string if it can't be
         converted.
       -----------------------------------------------------------------
    """
    # Error checking / set variables and initialize container.
    if type(string) != str:
        return string
    elif string[0] not in ["(", "[", "{"]:
        return string
    # end if
    open_char = string[0]
    if open_char == "{":
        close_char = "}"
        sep_char = ":"
        container = {}
    elif open_char == "(":
        close_char = ")"
        sep_char = ","
        container = tuple()
    else:
        close_char = "]"
        sep_char = ","
        container = []
    # end if
    if string[-1] != close_char:
        return string
    # end if
    # Empty container check.  If what was passed was a representation of
    #  an empty list/tuple/dictionary, just pass the appropriate empty
    #  container back.
    if string == "[]":
        return []
    elif string == "{}":
        return {}
    elif string == "()":
        return ()
    # Strip out container characters.
    while (string[0] == open_char) and (string[-1] == close_char):
        string = string[1:-1]
    # end while
    # Initialize pointers and flags.
    char = ""
    quote = False
    quote_char = ""
    level = 0
    start = 0
    pos = 0
    if type(container) == dict:
        d_flag = "key"
    # end if
    # Item parsing happens in an endless loop.
    while True:
        # Set start of current item.
        start = pos
        # Check to see if the first character is a quote mark.  If it
        #  is, mark the string as quoted (and advance the character
        #  pointer).
        if string[pos] in ["'", '"']:
            quote_char = string[pos]
            quote = True
            pos += 1
        # end if
        # Loop until hitting the next separator on the top level (or the
        #  end of the string).
        while (pos < len(string) and (
                (level > 0) or (quote) or (char != sep_char))):
            # Read a character.
            char = string[pos]
            # Opening and closing container characters.  The level flag
            #  shows whether the item is a nested container.
            if char in ["(", "[", "{"]:
                level += 1
            elif char in [")", "]", "}"]:
                level -= 1
            # If the character is a matching quote mark, turn off the
            #  quote flag, but only if it's not escaped.
            if (char == quote_char) and (string[pos - 1] != "\\"):
                quote = False
                quote_char = ""
            # end if
            # If we hit the separator on the top level or the end of the
            #  string, do NOT advance the character pointer.  BUT if we
            #  are parsing a quoted string, the separator can only come
            #  after the closing quote mark.
            elif (level == 0) and (not quote) and (char == sep_char):
                continue
            # end if
            pos += 1
            # end if
        # end while
        # Retrieve the complete item.
        item = string[start:pos]
        # Strip quote marks.
        if item[0] in ["'", '"'] and item[-1] == item[0]:
            item = item[1:-1]
        # end if
        # If the item is itself a container, the method calls itself to
        #  convert it.
        if item[0] in ["(", "[", "{"]:
            item = str_to_container(item)
        # Otherwise, try to convert to a number or boolean value.
        else:
            item = str_to_datetime(item)
            item = str_to_num(item)
            item = str_to_bool(item)
        # end if
        # Add the item to the container.  For a list, just append.
        if type(container) == list:
            container.append(item)
            # Tuples are immutable, so adding an item requires unpacking
            #  and repacking the entire tuple.  We use a temporary list
            #  for this.
        if type(container) == tuple:
            lst = []
            for x in container:
                lst.append(x)
            # end for
            lst.append(item)
            container = tuple(lst)
        # Dictionaries are the most complicated, because items are added
        #  in pairs.
        elif type(container) == dict:
            # Check the flag.  It if's set to "key"...
            if d_flag == "key":
                # Store the key.
                key_item = item
                # Change the separator.
                sep_char = ","
                # Flip the flag.
                d_flag = "value"
            # Else, add the key and value to the container.
            else:
                container[key_item] = item
                # Change the separator.
                sep_char = ":"
                # Flip the flag.
                d_flag = "key"
            # end if
        # Advance the pointer past the separator and any whitespace.
        pos += 1
        while (pos < len(string)) and (string[pos] == " "):
            pos += 1
        # end while
        char = ""
        # If we've reached the end of the string, we're done; break the
        #  loop.
        if pos >= len(string):
            break
    # end while
    # All done; return the container.
    return container
# end function


def str_to_num(string):
    """-----------------------------------------------------------------
        Takes a string representation of a number and converts it into a
        numeric type.

        Arguments:
        - string -- the string to convert.

        Returns:  a numeric type, if applicable; or the original
         string.
       -----------------------------------------------------------------
    """
    # Error check.
    if type(string) != str:
        return string
    str_num = string
    # Strip parentheses.
    while str_num[0] == "(" and str_num[-1] == ")":
        str_num = str_num[1:-1]
    # end while
    # Complex number.
    if re.search(r"[+-]?\d+(\.\d+)?[+-]{1}\d+(\.\d+)?j", str_num):
            return complex(str_num)
    # Floating point number.
    elif re.search(r"[+-]?\d+\.\d*(e\d*)?", str_num):
        return float(str_num)
    # Integer.
    elif re.fullmatch(r"[+-]?\d+", str_num):
        return int(str_num)
    else:
        return string
    # end if
# end function


def str_to_bool(string):
    """-----------------------------------------------------------------
        Takes a string representation of a boolean (True/False) and
         converts it to a bool type.  (Also checks for and converts
         None.)

        Arguments:
        - string -- the string to convert.

        Returns:  a bool type or None, if applicable; or the original
         string.
       -----------------------------------------------------------------
    """
    # Error check.
    if type(string) != str:
        return string
    if string == "True":
        return True
    elif string == "False":
        return False
    elif string == "None":
        return None
    else:
        return string
    # end if
# end function


def str_to_datetime(string):
    """-----------------------------------------------------------------
        Takes a string representation of a datetime, date, time, or
         timedelta object and converts it to the correct type.

        Arguments:
        - string -- the string to convert.

        Returns:  a valid datetime, date, time, or timedelta object, if
         possible, or the original string.
       -----------------------------------------------------------------
    """
    # Error check.
    if type(string) != str:
        return string
    # Check for date format.
    match = re.fullmatch(r"\d{4}-\d{2}-\d{2}", string)
    if match:
        # Put conversion in a try block in case the numbers aren't a
        #  valid date.
        try:
            return datetime.date.fromisoformat(string)
        except ValueError:
            return string
        except AttributeError:
            return _date_fromisoformat(string)
        # end try
    # Check for time format.
    match = re.fullmatch(r"\d{2}:\d{2}:\d{2}", string)
    if match:
        # Put conversion in a try block in case the numbers aren't a
        #  valid time.
        try:
            return datetime.time.fromisoformat(string)
        except ValueError:
            return string
        except AttributeError:
            return _time_fromisoformat(string)
        # end try
    # Check for datetime format.
    match = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", string)
    if match:
        # Put conversion in a try block in case the numbers aren't a
        #  valid datetime.
        try:
            return datetime.datetime.fromisoformat(string)
        except ValueError:
            return string
        except AttributeError:
            return _datetime_fromisoformat(string)
        # end try
    # Check for timedelta format.
    match = re.fullmatch(
          r"(?P<days>\d+)?( days, )?(?P<hours>\d{1,2}):(?P<minutes>\d{2})" +
          r":(?P<seconds>\d{2})", string)
    if match:
        # Make sure days isn't None.
        if not match.group("days"):
            d = "0"
        else:
            d = match.group("days")
        # end if
        # Put conversion in a try block in case the numbers aren't a
        #  valid timedelta.
        try:
            return datetime.timedelta(
              days=int(d),
              hours=int(match.group("hours")),
              minutes=int(match.group("minutes")),
              seconds=int(match.group("seconds")))
        except ValueError:
            return string
        # end try
    # If nothing matched, return the original string.
    return string
# end function


def _date_fromisoformat(string):
    """-----------------------------------------------------------------
        Creates a date object from a string, if that string is in the
         isoformat format.  Replicates the native date.fromisoformat
         method for environments below Python 3.7.

        Arguments:
        - string -- the string to check.

        Returns:  A date object if applicable, or the original
         string.
       -----------------------------------------------------------------
    """
    # Try to create a datetime object from the string.
    try:
        return datetime.datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError:
        return string
    # end try
# end function


def _datetime_fromisoformat(string):
    """-----------------------------------------------------------------
        Creates a datetime object from a string, if that string is in
         the isoformat format.  Replicates the native
         datetime.fromisoformat method for environments below Python
         3.7 (but only for strings formatted as produced by applying
         str() to a naive datetime object, or applying
         datetime.isoformat() to a naive datetime object with sep=' '.

        Arguments:
        - string -- the string to check.

        Returns:  A datetime object if applicable, or the original
         string.
       -----------------------------------------------------------------
    """
    # Try to create a datetime object from the string.
    try:
        # First try with microseconds.
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            # If that didn't work, try without microseconds.
            return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        # end try
        return string
    # end try
# end function


def _time_fromisoformat(string):
    """-----------------------------------------------------------------
        Creates a time object from a string, if that string is in the
         isoformat format.  Replicates the native date.fromisoformat
         method for environments below Python 3.7.

        Arguments:
        - string -- the string to check.

        Returns:  A time object if applicable, or the original
         string.
       -----------------------------------------------------------------
    """
    # Try to create a datetime object from the string.
    try:
        # First try with microseconds.
        return datetime.datetime.strptime(string, "%H:%M:%S.%f").time()
    except ValueError:
        try:
            # Then try without microseconds.
            return datetime.datetime.strptime(string, "%H:%M:%S").time()
        except ValueError:
            pass
        # end try
        return string
    # end try
# end function
