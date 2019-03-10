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
            l = []
            for x in container:
                l.append(x)
            # end for
            l.append(item)
            container = tuple(l)
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

def str_to_timedelta(string, sec=True):
    """-----------------------------------------------------------------
        Takes a string in standard timedelta format and creates a
         corresponding timedelta object.

        Arguments:
        - string -- the source string.
        - sec -- flag that informs the method that the expression
           includes seconds (default True).

        Returns:  the timedelta object, or None if the string isn't
         valid.
       -----------------------------------------------------------------
    """
    str_list=[]
    # First check to make sure it's a timedelta-formatted string, and
    #  return if it's not.
    if not re.fullmatch(
      r"(\d+ (day|days), )?(\d+:)?(\d{1,2})?:\d{2}", string):
        return None
    # Separate out days if it is present.
    str_list = string.split(", ")
    # Then split the hours:minutes:seconds, and set the days variable.
    if len(str_list) == 2:
        d = int(re.match(r"\d+", str_list[0]).group())
        td_list = str_list[1].split(":")
    else:
        # If days wasn't present, do the hh:mm:ss split and set the days
        #  variable to 0.
        d = 0
        td_list = str_list[0].split(":")
    # end if
    # What the elements of td_list represent depends on how many there
    #  are and the sec flag.
    if sec:
        if len(td_list) == 3:
            h = int(td_list[0])
            m = int(td_list[1])
            s = int(td_list[2])
        elif len(td_list) == 2:
            m = int(td_list[0])
            s = int(td_list[1])
        else:
            s = int(td_list[0])
        # end if
    else:
        s = 0
        # If sec is False but there are three elements, assume that the
        #  expression is in the non-standard but valid format dd:hh:mm.
        if len(td_list) == 3:
            d = int(td_list[0])
            h = int(td_list[1])
            m = int(td_list[2])
        elif len(td_list) == 2:
            h = int(td_list[0])
            m = int(td_list[1])
        else:
            m = int(td_list[0])
        # end if
    # end if
    # Range check.  Rather than returning as invalid an expression with
    #  elements that are out of range, "roll over" excess units to the
    #  next higher unit (consistent with timedelta's behavior).
    #  Negative numbers are still invalid, though.
    if s < 0:
        return None
    else:
        m += s // 60
        s = s % 60
    # end if
    if m < 0:
        return None
    else:
        h += m // 60
        m = m % 60
    # end if
    if h < 0:
        return None
    else:
        d += h // 24
        h = h % 24
    # end if
    # Create and return the timedelta object.
    return datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
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
