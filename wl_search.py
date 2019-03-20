"""---------------------------------------------------------------------
    Contains functions to find one or more entries based on user's
     criteria.

    Public Functions:
    - lookup_entry_by_id - finds an entry in the work log given its id
       number.
    - search_by_date -- searches for entries matching a datetime or
       range of datetimes.
    - search_by_duration -- searches for entries matching a duration or
       range of durations.
    - search_by_re -- searches for entries matching a regex string.
    - search_by_text -- searches for entries matching one or more
       search terms.
    - select_date -- displays a list of dates which contain tasks and
       asks the user to select one to view.
    - select_entry -- asks the user whether to browse through all
       matching entries, or select one from a list.

    Private Functions:
    - _find_entries_date - finds all entries that match a datetime or
       range of datetimes.
    - _find_entries_duration -- finds all entries that match a duration
       or range of durations.
    - _find_entries_re -- finds all entries matching a regex string.
    - _find_entries_text -- find all entries matching one or more
       search terms.
    - _get_date -- gets a date from the user.
    - _get_duration -- gets a duration from the user.
    - _get_time - gets a time from the user.
    - _match_item -- compares a search term to an entry to see if it
       matches.
    - _parse_string_text -- converts the user's search terms into a
       list that can be used as search criteria.
    - _z_exc -- generic exception handler.
   ---------------------------------------------------------------------
"""


# Import sys.
import sys


def _z_exc(loc, err):
    """-----------------------------------------------------------------
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
    import wl_datetime
    import wl_resource
    import wl_viewedit
except Exception as err:
    _z_exc("wl_search.py/module imports", err)
# end try


# Constants.
GO_BACK = -1
QUIT = 0
DATE = 1
DATE_RANGE = 2
DURATION = 1
DURATION_RANGE = 2
TITLE_SORT = 0
DATE_SORT = 1
SORT_KEY = 0
ENTRY_ID = 2
TITLE = 1
NOTES = 2
BOTH = 3


def lookup_entry_by_id(wl_obj, entry_id):
    """-----------------------------------------------------------------
        Finds a specific entry based on the entry's ID.

        Arguments:
        - wl_obj -- the work log object.
        - entry_id -- the ID of the entry to find.

        Returns:  the entry matching the ID, or None if there was no
         match.
       -----------------------------------------------------------------
    """
    try:
        # Since the entry IDs aren't in any order, we have to just go
        #  through the entire list until a match is found.
        for entry in wl_obj.entries:
            if entry.id == entry_id:
                return entry
            # end if
        # end for
        # If no match, return None.
        return None
    except Exception as err:
        _z_exc("wl_search.py/lookup_entry_by_id", err)
    # end try
# end function


def search_by_date(wl_obj):
    """-----------------------------------------------------------------
        Finds work log entries based on a date/time or date/time range.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  for searches by date/time, a list of matching entries
         from the date-sorted index, if any are found, an empty list if
         no matches are found, or None if the user aborts; for a view of
         all dates, a list of unique date objects.
       -----------------------------------------------------------------
    """
    try:
        # Run everything inside a loop in case the user wants to start
        #  over.
        while True:
            # Option menu.
            search_mode = io_utils.menu(
              ["A single date/time", "A range of dates/times",
               "View all dates"], keystroke_list="#",
              prompt="How would you like to search?",
              line_length=wl_obj.line_length)
            # User quits, just exit.
            if search_mode == QUIT:
                return None
            # end if
            if search_mode in [DATE, DATE_RANGE]:
                # Both date/time searches require at least one date.
                if search_mode == DATE:
                    d_type = "single"
                else:
                    d_type = "start"
                # end if
                # Get the first (and for a single date/time search,
                #  only) date/time.
                go, date = _get_date(wl_obj, d_type)
                # If the user decided to go back here, loop back.
                if go == GO_BACK:
                    continue
                # end if
                # If the user decided to abort, confirm and then return.
                if go == QUIT and io_utils.confirm("abort the search"):
                    return None
                # end if
                # Now get a time, if the user wants one.
                go, date = _get_time(wl_obj, d_type, date)
                # If the user decided to go back here, loop back.
                if go == GO_BACK:
                    continue
                # end if
                # If the user decided to abort, confirm and then return.
                if go == QUIT and io_utils.confirm("abort the search"):
                    return None
                # end if
                # If the user declined to enter a time, set the time of
                #  the datetime object to midnight.
                if type(date) == datetime.date:
                    start_date = datetime.datetime.combine(
                      date, datetime.time())
                # end if
                # If the user wants to search a single date/time...
                if search_mode == DATE:
                    # If the user wants to search a specific date AND
                    #  time, set the end of the range to equal the
                    #  start.
                    if type(date) == datetime.datetime:
                        end_date = start_date
                    # If the user wants to search a particular date but
                    #  not a particular time, set the end of the range
                    #  to 11:59pm on the same date as the start.
                    else:
                        end_date = start_date.replace(hour=23, minute=59)
                    # end if
                # If searching a range, get the end date from the user.
                else:
                    go, date = _get_date(wl_obj, "end", start=start_date)
                    # If the user decided to go back here, loop back.
                    if go == GO_BACK:
                        continue
                    # end if
                    # If the user decided to abort, confirm and then
                    #  return.
                    if go == QUIT and io_utils.confirm("abort the search"):
                        return None
                    # end if
                    # Now get a time, if the user wants one.
                    go, date = _get_time(wl_obj, "end", date)
                    # If the user decided to go back here, loop back.
                    if go == GO_BACK:
                        continue
                    # end if
                    # If the user decided to abort, confirm and then
                    #  return.
                    if go == QUIT and io_utils.confirm("abort the search"):
                        return None
                    # end if
                    # If the user declined to enter a time, set the time
                    #  of the datetime object to the end of the day.
                    if type(date) == datetime.date:
                        end_date = datetime.datetime.combine(
                          date, datetime.time.max)
                    # end if
                # end if
                # Return the entries to match the search terms.
                return_list = _find_entries_date(wl_obj, start_date, end_date)
                # If nothing was found, tell the user.
                if len(return_list) == 0:
                    io_utils.print_status(
                      "Status", "No matches found.",
                      line_length=wl_obj.line_length)
                # end if
                return return_list
            # To view all dates, create a list of unique dates.
            else:
                return_list = []
                # Iterate through the sorted list.
                for entry in wl_obj.sorts[DATE_SORT]:
                    # Convert datetime to date and append all unique
                    #  dates.
                    if entry[SORT_KEY].date() not in return_list:
                        return_list.append(entry[SORT_KEY].date())
                    # end if
                # end for
                return return_list
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/search_by_date", err)
    # end try
# end function


def search_by_duration(wl_obj):
    """-----------------------------------------------------------------
        Finds work log entries based on a duration or duration range.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  a list of matching entries, if any are found; else an
         empty list.
       -----------------------------------------------------------------
    """
    try:
        # Run everything inside a loop in case the user wants to start
        #  over.
        while True:
            # Option menu.
            search_mode = io_utils.menu(
              ["A specific duration", "A range of durations"],
              keystroke_list="#", prompt="What would you like to search?",
              line_length=wl_obj.line_length)
            # User quits, just exit.
            if search_mode == QUIT:
                return None
            # end if
            # Both single duration and range require one duration, so
            #  get one now.
            if search_mode == DURATION:
                d_type = "single"
            else:
                d_type = "minimum"
            # end if
            go, min_duration = _get_duration(wl_obj, d_type)
            # If the user wants to go back, loop back to the beginning.
            if go == GO_BACK:
                continue
            # If the user aborts, return.
            elif go == QUIT:
                return []
            # end if
            # If the user wants to search a range, get a maximum
            #  duration.
            if search_mode == DURATION_RANGE:
                d_type = "maximum"
                go, max_duration = _get_duration(wl_obj, d_type, min_duration)
                # Again, loop back or return if the user chooses to go
                #  back or abort.
                if go == GO_BACK:
                    continue
                elif go == QUIT:
                    return []
                # end if
            # If the search is for a single duration, just set the
            #  maximum duration to equal the minimum.
            else:
                max_duration = min_duration
            # end if
            # Now find all entries that match.
            r_list = _find_entries_duration(wl_obj, min_duration, max_duration)
            # If no matches, tell the user.
            if len(r_list) == 0:
                io_utils.print_status(
                  "Status", "No matches found.",
                  line_length=wl_obj.line_length)
            # end if
            return r_list
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/search_by_duration", err)
    # end try
# end function


def search_by_re(wl_obj):
    """-----------------------------------------------------------------
        Finds work log entries based on a regular expression.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  a list of matching entries, if any are found; else an
         empty list.
       -----------------------------------------------------------------
    """
    try:
        # Run everything inside a loop in case the user wants to start
        #  over.
        while True:
            wl_obj.help.print_help(
              wl_obj.show_help, "RE Search", "_sh_re",
              line_length=wl_obj.line_length)
            # Get a regex string.
            re_string = io_utils.get_input(
              "Enter a regular expression (without quotation marks):")
            # If the user chose to toggle help, do that.
            if re.match(r"-h", re_string, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # end if
            # If the user didn't enter anything...
            if not re_string:
                io_utils.print_status(
                  "Error", "You did not enter anything.", go=True,
                  line_length=wl_obj.line_length)
                if not io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    return []
                else:
                    continue
                # end if
            # end if
            # Option menu.
            search_mode = io_utils.menu(
              ["Title", "Notes", "Title and Notes"], keystroke_list="#",
              prompt="Which field(s) would you like to search?",
              line_length=wl_obj.line_length)
            # User quits, just exit.
            if search_mode == QUIT:
                return None
            # end if
            # Get the results of the find function.
            return_list = _find_entries_re(wl_obj, re_string, search_mode)
            # If nothing matched, tell the user.
            if len(return_list) == 0:
                io_utils.print_status(
                  "Status", "No matches found.",
                  line_length=wl_obj.line_length)
            # end if
            return return_list
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/search_by_re", err)
    # end try
# end function


def search_by_text(wl_obj):
    """-----------------------------------------------------------------
        Finds work log entries based on a text string.

        Arguments:
        - wl_obj -- the work log object.

        Returns:  a list of matching entries, if any are found; else an
         empty list.
       -----------------------------------------------------------------
    """
    try:
        # Run everything inside a loop in case the user wants to start
        #  over.
        while True:
            # Option menu.
            search_fields = io_utils.menu(
              ["Title", "Notes", "Title and Notes"], keystroke_list="#",
              prompt="Which field(s) would you like to search?",
              line_length=wl_obj.line_length)
            # User quits, just exit.
            if search_fields == QUIT:
                return None
            # end if
            # Print the instructions.
            wl_obj.help.print_help(
              wl_obj.show_help, "Search Terms", "_sh_text",
              line_length=wl_obj.line_length)
            # Get a text string to search for.
            search_string = io_utils.get_input("Enter text to search for:")
            # If the user chose to toggle help, do that.
            if re.match(r"-h", search_string, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user didn't enter anything, either loop back or
            #  return.
            if not search_string:
                print("You did not enter anything.")
                if not io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    return []
                else:
                    continue
                # end if
            # end if
            # If the search string includes wildcard characters, ask the
            #  user how to treat them.
            if re.search(r"[?*]", search_string):
                search_mode = io_utils.menu(
                  ["Literal search (? and * will only match themselves)",
                   "Wildcard search (? and * will match any character)"],
                  prompt="Your search string contains one or more wildcard " +
                  "characters (? or *).  What kind of search would you " +
                  "like to perform?", keystroke_list="#",
                  line_length=wl_obj.line_length)
                # If the user chooses to go back, start over.
                if search_mode == QUIT:
                    continue
                # end if
            # Set the default to literal search.
            else:
                search_mode = 1
            # Return the results of the find function.
            return_list = _find_entries_text(
              wl_obj, search_string, search_fields, search_mode)
            # If nothing matched, tell the user.
            if len(return_list) == 0:
                io_utils.print_status(
                  "Status", "No matches found.",
                  line_length=wl_obj.line_length)
            # end if
            return return_list
        # end while
    except Exception as err:
        _z_exc("wl_search.py/search_by_text", err)
    # end try
# end function


def select_date(wl_obj, date_list):
    """-----------------------------------------------------------------
        Show a list (or part of a list) of dates that contain log
         entries.

        Arguments:
        - wl_obj -- the work log object.
        - date_list -- the list of dates.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        start = 0
        # Clear the screen.
        wl_resource.print_header(wl_obj)
        # Print the number of dates found.
        if len(date_list) == 1:
            msg = "Found 1 date with entries."
        else:
            msg = f"Found {len(date_list)} dates with entries."
        # end if
        io_utils.print_status("Status", msg, line_length=wl_obj.line_length)
        # Run in a loop until the user is done viewing/editing, then
        #  return.
        while True:
            # Call list browse.
            response = wl_viewedit.browse_list(wl_obj, date_list, start=start)
            # If the response isn't an integer, it's a command to move
            #  forward or back.  Move the start position, but only if it
            #  doesn't go beyond the bounds of the list.
            if type(response) == str:
                if (response.upper() == "P") and (start - 9 >= 0):
                    start -= 9
                elif (
                  (response.upper() == "N") and (start + 9 < len(date_list))):
                    start += 9
                # end if
                # Clear the screen before looping back.
                wl_resource.print_header(wl_obj)
                continue
            # end if
            # If the user quits, return.
            if response == QUIT:
                return
            # end if
            # If it's a non-zero integer, the user chose a date.  Find
            #  all entries on that date.
            start_date = datetime.datetime.combine(
              date_list[start + response - 1], datetime.time())
            end_date = start_date.replace(hour=23, minute=59)
            entry_list = _find_entries_date(wl_obj, start_date, end_date)
            # Let the user browse/edit those entries. (If the user
            #  edited the list, it will come back changed.)
            entry_list = wl_viewedit.browse_entries(wl_obj, entry_list)
            # If the user deleted all of the entries for a date, then
            #  that date is no longer valid and must be removed.
            if len(entry_list) == 0:
                del date_list[start + response - 1]
            # end if
            # Clear the screen before looping back.
            wl_resource.print_header(wl_obj)
        # end while
    except Exception as err:
        _z_exc("wl_search.py/select_date", err)
    # end try
# end function


def select_entry(wl_obj, entry_list):
    """-----------------------------------------------------------------
        Allows the user to either browse a set of entries, or choose
         from a list.

        Arguments:
        - wl_obj -- the work log object.
        - entry_list -- the list of entries.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen.
        wl_resource.print_header(wl_obj)
        # Print the number of dates found.
        if len(entry_list) == 1:
            msg = "Found 1 task."
        else:
            msg = f"Found {len(entry_list)} tasks."
        # end if
        io_utils.print_status("Status", msg, line_length=wl_obj.line_length)
        # Ask the user to browse or pick from list.
        response = io_utils.menu(
          ["Browse all matching tasks",
           "Choose from a list of matching tasks"], keystroke_list="#",
          quit_=True,
          prompt="Please select how you want to see the matching tasks:",
          line_length=wl_obj.line_length)
        # If the user chooses to go back, just return.
        if response == QUIT:
            return
        # end if
        # If the user chooses to browse the matches, call the browse
        #  function, then return.
        if response == 1:
            entry_list = wl_viewedit.browse_entries(wl_obj, entry_list)
            return
        # If the user chooses to see a list, display it here.
        else:
            start = 0
            # Run in a loop until the user is done viewing/editing, then
            #  return.
            while True:
                # Call list browse.
                response = wl_viewedit.browse_list(
                  wl_obj, entry_list, start=start)
                # If the response isn't an integer, it's a command to
                #  move forward or back.  Move the start position, but
                #  only if it doesn't go beyond the bounds of the list.
                if type(response) == str:
                    if (response.lower() == "p") and (start - 9 >= 0):
                        start -= 9
                    elif (
                      (response.lower() == "n") and
                      (start + 9 < len(entry_list))):
                        start += 9
                    # end if
                    # Clear the screen before looping back.
                    wl_resource.print_header(wl_obj)
                    continue
                # end if
                # If the user quits, return.
                if response == QUIT:
                    return
                # end if
                # If it's a non-zero integer, the user chose an entry.
                #  Get the index number of the chosen entry in the list.
                ndx = start + response - 1
                # Browse entries, starting with the selected one.
                wl_viewedit.browse_entries(wl_obj, entry_list, ndx=ndx)
                # Clear the screen before looping back.
                wl_resource.print_header(wl_obj)
            # end while
        # end if
    except Exception as err:
        _z_exc("wl_search.py/select_entry", err)
    # end try
# end function


def _find_entries_date(wl_obj, start_date, end_date):
    """-----------------------------------------------------------------
        Finds entries matching a date/time or range of date/times.

        Arguments:
        - wl_obj -- the work log object.
        - start_date -- the starting date/time to search.
        - end_date -- the ending date/time to search.

        Returns:  a list of entries matching the date or date range, or
         an empty list if no matches are found.
       -----------------------------------------------------------------
    """
    try:
        return_list = []
        # NOTE:  Because the work logs used by this program are not
        #  likely to contain a large number of entries, the program uses
        #  a brute-force search method.  For logs containing hundreds to
        #  thousands of entries, a dynamic search algorithm might be
        #  more efficient.
        #
        # Brute-force search:  start at the beginning, run until
        #  reaching the end or passing the date range.
        for ndx, entry in enumerate(wl_obj.sorts[DATE_SORT]):
            # If the entry matches the date/time or falls within the
            #  range:
            if start_date <= entry[SORT_KEY] <= end_date:
                return_list.append(lookup_entry_by_id(wl_obj, entry[ENTRY_ID]))
            # If the list is past the range, quit looking.
            if entry[SORT_KEY] > end_date:
                break
            # end if
        # end for
        return return_list
    except Exception as err:
        _z_exc("wl_search.py/_find_entries_date", err)
    # end try
# end function


def _find_entries_duration(wl_obj, min_duration, max_duration):
    """-----------------------------------------------------------------
        Finds entries matching a duration.

        Arguments:
        - wl_obj -- the work log object.
        - start_date -- the starting date/time to search.
        - end_date -- the ending date/time to search.

        Returns:  a list of matching entries, or an empty list if no
         matches were found.
       -----------------------------------------------------------------
    """
    try:
        return_list = []
        # Since entries aren't indexed by duration, the search needs to
        #  be brute-force, and can't be direct.  But using the date-
        #  sorted index will cause the list of returned entries to be in
        #  date order.
        #
        # Loop through every entry.
        for entry in wl_obj.sorts[DATE_SORT]:
            # If the entry's duration falls within the range, add it.
            current = lookup_entry_by_id(wl_obj, entry[ENTRY_ID])
            if (
              current and (min_duration <= current.duration <= max_duration)):
                return_list.append(current)
            # end if
        # end for
        # Return the list.
        return return_list
    except Exception as err:
        _z_exc("wl_search.py/_find_entries_duration", err)
    # end try
# end function


def _find_entries_re(wl_obj, pattern, fields):
    """-----------------------------------------------------------------
        Finds entries matching a regular expression.

        Arguments:
        - wl_obj -- the work log object.
        - pattern -- the regular expression to search.
        - fields -- the field(s) to search.

        Returns:   a list of matching entries, or an empty list if no
         matches were found.
       -----------------------------------------------------------------
    """
    try:
        return_list = []
        # If the user has specified a case-insensitive search--
        # Make sure the pattern is valid.
        if re.search(r", re\.I", pattern):
            # Slice off the flag.1
            pattern = pattern[:-6]
            try:
                pattern = re.compile(pattern, re.I)
            except Exception:
                io_utils.print_status(
                  "Error", f"{pattern} failed to compile.", go=True)
                return []
            # end try
        else:
            try:
                pattern = re.compile(pattern)
            except Exception:
                io_utils.print_status(
                  "Error", f"{pattern} failed to compile.", go=True)
                return []
            # end try
        # end if
        for entry in wl_obj.entries:
            if (
              ((fields in [TITLE, BOTH]) and
               (re.search(pattern, entry.title))) or
              ((fields in [NOTES, BOTH]) and
               (re.search(pattern, entry.notes)))):
                return_list.append(entry)
            # end if
        # end for
        return return_list
    except Exception as err:
        _z_exc("wl_search.py/find_entries_re", err)
    # end try
# end function


def _find_entries_text(wl_obj, string, fields, mode):
    """-----------------------------------------------------------------
        Finds entries based on a text string.

        Arguments:
        - wl_obj -- the work log object
        - string -- the text to search for.
        - fields -- which field(s) to search.
        - mode -- the type of search to conduct.

        Returns:  two lists, one of literal matches and one of wildcard
         matches.  Either list will be empty if there are no matches.
       -----------------------------------------------------------------
    """
    try:
        # Set the mode selector.
        if mode == 2:
            wildcard = True
        else:
            wildcard = False
        # end if
        # The string needs to be sorted into a format in which each
        #  element can be searched for correctly.
        query = _parse_search_text(string, wildcard=wildcard)
        # Go through the whole log, checking each entry.
        return_list = []
        for entry in wl_obj.sorts[TITLE_SORT]:
            current = lookup_entry_by_id(wl_obj, entry[ENTRY_ID])
            if _match_item(query, current, fields):
                return_list.append(current)
            # end if
        # end for
        return return_list
    except Exception as err:
        _z_exc("wl_search.py/find_entries_text", err)
    # end try
# end function


def _get_date(wl_obj, d_type, start=None):
    """-----------------------------------------------------------------
        Gets a date from the user.

        Arguments:
        - wl_obj -- the work log object.
        - d_type -- which date to prompt for (single, start, end).

        Keyword Arguments:
        - start -- starting date (for error checking).

        Returns:  1) an integer representing the return state: -1 if the
         user chose to go back, 0 if the user chose to abort completely,
         1 if the user successfully entered a date; 2) a date object, or
         None if the user chose to quit or go back.
       -----------------------------------------------------------------
    """
    try:
        # Set the prompt.
        if d_type == "single":
            prompt = "Enter the date on which to search:"
        elif d_type == "start":
            prompt = "Enter the starting date for your search:"
        else:
            prompt = "Enter the ending date for your search:"
        # end if
        # Loop until a valid date is obtained or the user aborts.
        while True:
            # Get the date.
            response = io_utils.get_input(prompt)
            # Error prompt.
            msg = "You did nol enter anything."
            # If the user entered something, parse it.
            if response:
                date = wl_datetime.parse_date_input(wl_obj, response)
                if date:
                    if d_type != "end":
                        return 1, date
                    else:
                        if date >= start.date():
                            return 1, date
                        elif date and date < start.date():
                            # Alternate error message.
                            msg = (
                              "The end date cannot be ealier than " +
                              f"{start.date}")
                            io_utils.print_status(
                              "Error", msg, line_length=wl_obj.line_length)
                        # end if
                    # end if
                # end if
            retry = io_utils.yes_no(
              "Try again?", quit_=True, line_length=wl_obj.line_length)
            # If the user decides not to try again, return.  (Not trying
            #  again here is treated as equivalent to going back.)
            if retry in ["-b", False]:
                return -1, None
            elif retry == "-q":
                return 0, None
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/_get_date", err)
    # end try
# end function


def _get_duration(wl_obj, d_type, start=None):
    """-----------------------------------------------------------------
        Gets a duration from the user.

        Arguments:
        - wl_obj -- the work log object.
        - d_type -- the type of duration to get (single, min, max)

        Keyword Arguments:
        - start -- the min duration (for error checking).

        Returns:  1) an integer representing the return state: -1 if the
         user chose to go back, 0 if the user chose to abort completely,
         1 if the user successfully entered a duration; 2) if the user
         enters a valid duration, a timedelta object representing that
         duration; else None.
       -----------------------------------------------------------------
    """
    try:
        # Build prompt.
        if d_type == "single":
            p = ""
        else:
            p = f"{d_type} "
        # end if
        prompt = f"Enter the {p}duration to search for"
        if start:
            prompt += (
              ".  To search for ALL durations of " +
              f"{wl_resource.format_string(wl_obj, start)} or greater, " +
              "enter [max]:")
        else:
            prompt += ":"
        # Loop until a valid response is obtained.
        while True:
            # Get a duration.
            response = io_utils.get_input(prompt)
            if response == "-b":
                return -1, None
            elif response == "-q":
                return 0, None
            # end if
            # Parse the input for a duration.
            duration = wl_datetime.calc_duration_abs(wl_obj, response)
            # If no valid duration was entered, print error and prompt
            #  to try again.
            if duration is None:
                msg = (
                  f"{response} could not be interpreted as a valid duration.")
                io_utils.print_status(
                  "Error", msg, line_length=wl_obj.line_length)
                # Take a "no" as equivalent of the user aborting.
                if not io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    return 0, None
                # If "yes", loop back.
                else:
                    continue
                # end if
            # end if
            return 1, duration
        # end while
    except Exception as err:
        _z_exc("wl_search.py/_get_duration", err)
    # end try
# end function


def _get_time(wl_obj, t_type, date, start=None):
    """-----------------------------------------------------------------
        Gets a time from the user.

        Arguments:
        - wl_obj -- the work log object.
        - t_type -- which date is being modified (single, start, end)
        - date -- the date object to which to append the time.

        Keyword Arguments:
        - start -- the starting date/time (for error checking).

        Returns:  1) an integer representing the return state: -1 if the
         user chose to go back, 0 if the user chose to abort completely,
         1 if the user successfully entered a date; 2) if the user
         enters a valid time, a datetime object with the original date
         combined with the time; otherwise, the original date object.
       -----------------------------------------------------------------
    """
    try:
        # Prompt.
        if t_type == "single":
            t_type = "conduct"
        # end if
        # Build prompt.
        prompt = (
          f"If you would like to {t_type} your search at a specific time" +
          f" during {wl_resource.format_string(wl_obj, date, short=True)}, " +
          "enter the time now, or just press [ENTER] to include the entire " +
          "day:")
        # Loop until a valid response is obtained.
        while True:
            # Get a time.
            response = io_utils.get_input(prompt, must_respond=False)
            # If the user didn't enter anything, just return the date.
            #  (Since the caller will set the time to 11:59pm, it will
            #  never be earlier than the starting time.)
            if not response:
                return 1, date
            # end if
            # Return None if the user wants to quit.
            if response.lower() == "-b":
                return -1, None
            # end if
            # Otherwise parse the input for a time.
            time = wl_datetime.parse_time_input(wl_obj, response)
            msg = f"{response} could not be interpreted as a valid time."
            # If a time was found, combine it with the date and return,
            #  unless--
            if time:
                # If the start and end dates are different, the times
                #  are irrelevant.
                if date.date > start.date:
                    return 1, datetime.datetime.combine(date, time)
                # If the start and end dates are the same, the end time
                #  cannot precede the start time.
                else:
                    if time >= start.time:
                        return 1, datetime.datetime.combine(date, time)
                    else:
                        msg = (
                          f"The end time cannot be earlier than {start.time}")
                    # end if
                # end if
            # end if
            # Print an error message, ask the user if they want to try
            #  again, and if they say no, return None (else loop back).
            io_utils.print_status("Error", msg, line_length=wl_obj.line_length)
            retry = io_utils.yes_no(
              "Try again?", quit_=True, line_length=wl_obj.line_length)
            if retry in ["-b", False]:
                return -1, None
            elif retry == "-q":
                return 0, None
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/_get_time", err)
    # end try
# end function


def _match_item(item, entry, mode):
    """-----------------------------------------------------------------
        Looks for a match between a query and a log entry's title,
         notes, or both.

        Arguments:
        - item -- the query, which will either be a list or a tuple.
        - entry -- the log entry to search.
        - mode -- the field(s) to search.

        Returns:  True if the query matches, False if not.
       -----------------------------------------------------------------
    """
    try:
        # Storage for search results.
        match_list = [None for _ in range(len(item))]
        # Check each item in the term.
        for ndx, subitem in enumerate(item):
            # If the item is itself a list or tuple, recursively call
            #  this function to search it.
            if type(subitem) in (list, tuple):
                match_list[ndx] = _match_item(subitem, entry, mode)
            # Search the fields indicated.
            else:
                if (
                  ((mode == TITLE) and
                   re.search(subitem, entry.title, re.I)) or
                  ((mode == NOTES) and
                   re.search(subitem, entry.notes, re.I)) or
                  ((mode == BOTH) and
                   (re.search(subitem, entry.title, re.I) or
                   re.search(subitem, entry.notes, re.I)))):
                    match_list[ndx] = True
                else:
                    match_list[ndx] = False
                # end if
            # end if
        # end for
        # Evaluate and return the results.  If the query is a list (OR
        #  search), it matches if any of its terms matched.  If the query is
        #  a tuple (AND search), it matches only if all of its terms
        #  matched.
        if (
          ((type(item) == list) and (True in match_list)) or
          ((type(item) == tuple) and (False not in match_list))):
            return True
        else:
            return False
        # end if
    except Exception as err:
        _z_exc("wl_search.py/_match_item", err)
    # end try
# end function


def _parse_search_text(string, wildcard=False):
    """-----------------------------------------------------------------
        Takes a string containing search terms and formats it for the
         search function.

        Arguments:
        - string -- the string to parse.

        Keyword Arguments:
        - wildcard -- if True, convert wildcard characters in the
           string.

        Returns:  a formatted list.
       -----------------------------------------------------------------
    """
    try:
        # Since the search terms in the string will eventually become
        #  regex patterns, before doing anything, make sure that any
        #  backslashes in the string are escaped.
        string = string.replace("\\", "\\\\")
        # If searching with wildcards, convert any wildcard characters
        #  in the string to their regex equivalents.
        if wildcard:
            string = string.replace("?", "\\w")
            string = string.replace("*", "\\w*")
        # If NOT searching with wildcards, make sure any wildcard
        #  characters are escaped, so that they are searched for
        #  literally.
        else:
            string = string.replace("?", r"\?")
            string = string.replace("*", r"\*")
        # end if
        return_list = []
        tup_stor = []
        # Parsing goes from left to right.
        pos = 0
        while pos < len(string):
            start = pos
            end = 0
            element = ""
            lvl = 0
            # If an opening quote mark is found, locate the closing
            #  quote mark.  Note that parentheses inside quote marks do
            #  not group.
            if string[pos] == '"':
                while True:
                    pos += 1
                    if pos == len(string):
                        break
                    # end if
                    if (string[pos] == " ") and (string[pos - 1] == '"'):
                        break
                    # end if
                # end while
                end = pos
            # If an opening parenthesis is found, locate the closing
            #  parenthesis (but note that additional sets of parentheses
            #  can be nested inside).
            elif string[pos] == "(":
                lvl = 1
                while True:
                    pos += 1
                    if pos == len(string):
                        break
                    # end if
                    if (string[pos] == "(") and (string[pos - 1] == " "):
                        lvl += 1
                    elif (string[pos] == " ") and (string[pos - 1] == ')'):
                        lvl -= 1
                    # end if
                    if (lvl == 0):
                        break
                    # end if
                # end while
                end = pos
            # If there is neither a quote mark or a parenthesis, just
            #  find the end of the word.
            else:
                while True:
                    pos += 1
                    if (pos == len(string)) or string[pos] == " ":
                        break
                    # end if
                # end while
                end = pos
            # end if
            # Now pull the substring from the string.
            element = string[start:end]
            # If the substring is in quotes, just strip them.
            if element[0] == '"':
                element = element[1:-1]
            # if the substring is in parentheses, strip them and then
            #  call the function recursively to produce a subitem.
            elif element[0] == "(":
                element = element[1:-1]
                element = _parse_search_text(element)
            # end if
            # If the substring is part of a larger AND item, add it.
            if tup_stor:
                tup_stor.append(element)
            # end if
            # Advance the pointer to the next non-space character, or
            #  the end of the string.
            while (pos < len(string)) and (string[pos] == " "):
                pos += 1
            # end while
            # If we are at the end of the string...
            if pos == len(string):
                # If there is an AND item stored, create a tuple from it
                #  and add it to the return list.
                if tup_stor:
                    return_list.append(tuple(tup_stor))
                # Else append the substring to the return list.
                else:
                    return_list.append(element)
                # end if
                # Return the list.
                return return_list
            # end if
            # See if the following character(s) are a plus sign or the
            #  word "and".
            if (string[pos] == "+") or (string[pos:pos+3].lower() == "and"):
                # If the substring is the start of an AND item, store
                #  it.  If it's a continuation of an AND item, it's
                #  already stored.
                if not tup_stor:
                    tup_stor.append(element)
                # end if
                # And loop back for the next substring.
            # Otherwise, the item is complete.  Append either the AND
            #  item or the element to the return list and loop back.
            else:
                if tup_stor:
                    return_list.append(tuple(tup_stor))
                    tup_stor = []
                else:
                    return_list.append(element)
                # end if
            # end if
            # Before looping back, move the counter past any operator.
            m = re.match(r"(and\s+)|(or\s+)|(\|\s+)|(\+\s+)", string[pos:])
            if m:
                pos += m.end()
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_search.py/_parse_search_text", err)
    # end try
# end function
