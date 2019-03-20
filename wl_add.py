"""---------------------------------------------------------------------
    Contains functions to initialize or update the attributes of a log
     entry object via user input.

    Public Functions:
    - add_date -- sets the log entry object's date attribute.
    - add_datetime -- sets the log entry object's datetime attribute.
    - add_duration -- sets the log entry object's duration attribute.
    - add_note -- sets the log entry object's notes attibute.
    - add_recurrance -- sets the log entry object's recurrance
       attribute.
    - add_time -- sets the log entry object's time attribute.
    - add_title -- sets the log entry object's title attribute.

    Private Functions:
    - _find_recurrances -- sets the interval or conditions that a task
       will recur.
    - _get_dates -- gets a list of integers from the user, representing
       days of the month.
    - _screen_reset -- clears the screen, prints the program header, and
       for the current task being added, displays the attributes which
       have been set.
    - _screen_reset_edit -- clears the screen, prints the program
       header, and for the current task being edited, displays the
       task's attributes, including changes which have been made by the
       user.
    - _set_occurances -- gets an end date for a task's recurrance, and
       calculates the dates on which the task will recur.
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
    sys.exit(
      "Please report the above error and the circumstances which caused it " +
      "to the developer.")
    return
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
    _z_exc("wl_add.py/module imports", err)
# end try


# Constants.
DAILY = 1
WEEKLY = 2
MONTHLY = 3


def add_date(wl_obj, entry, edit=False):
    """-----------------------------------------------------------------
        Gets the user's input for a task date, then sets the log entry's
         attribute.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Keyword Arguments:
        - edit -- edit an existing entry (default False)

        Returns:  1 if successful, 0 if the user chooses to abort, or
         -1 if the user chooses to go back.
       -----------------------------------------------------------------
    """
    try:
        # Run in a loop until valid date is obtained.
        valid = False
        while not valid:
            # First set the date format if necessary.
            if not wl_obj.date_format:
                wl_datetime.set_endian(wl_obj)
            # end if
            # Refresh the entry's attributes.
            if edit:
                _screen_reset_edit(wl_obj, entry)
            else:
                _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # end if
            # Print the appropriate help text.
            wl_obj.help.print_help(
              wl_obj.show_help, "Task Date", "_ah_date",
              line_length=wl_obj.line_length)
            # Print navigational instructions.
            if not edit:
                wl_resource.print_nav(q=True, b=True)
            # end if
            # Set prompt.
            if edit:
                prompt = (
                  "Please enter a new date for this task, or press [ENTER] " +
                  "to leave the date unchanged:")
            else:
                prompt = "Please enter the date for this task:"
            # Print the prompt and get the response.
            response = io_utils.get_input(prompt, must_respond=False)
            # If editing, exit if the user didn't enter anything.
            if edit and response == "":
                return 0
            # end if
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0
            # If the user chose to go back, also exit.
            elif re.match(r"-b", response, re.I):
                return -1
            # If the user chose to toggle help, do that.
            elif re.match(r"-h", response, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user just hit Enter, set the date to today.
            elif response == "":
                entry.date = datetime.date.today()
                valid = True
            # Otherwise parse the string to determine the date.
            else:
                entry_date = wl_datetime.parse_date_input(wl_obj, response)
                if entry_date:
                    entry.date = entry_date
                    valid = True
                # end if
            # end if
        # end while
        return 1
    except Exception as err:
        _z_exc("wl_add.py/add_date", err)
    # end try
# end function


def add_datetime(entry):
    """-----------------------------------------------------------------
        Takes an entry's date and time attributes and combines them.

        Arguments:
        - entry -- the log entry object.

        Returns:  nothing
       -----------------------------------------------------------------
    """
    try:
        return datetime.datetime.combine(entry.date, entry.time)
    except Exception as err:
        _z_exc("wl_add.py/add_datetime", err)
    # end try
# end function


def add_duration(wl_obj, entry, edit=False):
    """-----------------------------------------------------------------
        Gets the user's input for a task duration, then sets the log
         entry's attribute.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Keyword Arguments:
        - edit -- edit an existing entry (default False)

        Returns:  1 if successful, 0 if the user chooses to abort, or
         -1 if the user chooses to go back.
       -----------------------------------------------------------------
    """
    try:
        # Run in a loop until valid duration or end time is obtained.
        valid = False
        while not valid:
            # Refresh the entry's attributes.
            if edit:
                _screen_reset_edit(wl_obj, entry)
            else:
                _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # end if
            # Print the appropriate help text.
            wl_obj.help.print_help(
              wl_obj.show_help, "Task Duration", "_ah_duration",
              line_length=wl_obj.line_length)
            # Print navigational instructions.
            if not edit:
                wl_resource.print_nav(q=True, b=True)
            # end if
            # Build prompt.
            if edit:
                prompt = (
                  "Please enter a new duration or end time for this task, " +
                  "or press [ENTER] to leave the duration unchanged:")
            else:
                prompt = (
                  "Please enter the duration or end time for this task:")
            # Print the prompt and get the response.
            response = io_utils.get_input(prompt, must_respond=False)
            # If editing and the user didn't enter anything, return.
            if edit and response == "":
                return 0
            # end if
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0
            # If the user chose to go back, also exit.
            elif re.match(r"-b", response, re.I):
                return -1
            # If the user chose to toggle help, do that.
            elif re.match(r"-h", response, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user didn't enter anything (and isn't editing),
            #  show an error message and loop back.
            elif response == "":
                io_utils.print_status(
                  "Error", "You did not enter anything.",
                  line_length=wl_obj.line_length)
                continue
            # end if
            # Otherwise parse the string to determine the time.
            else:
                duration = wl_datetime.parse_duration_input(
                  wl_obj, entry, response)
            # end if
            if duration is not None:
                valid = True
            else:
                msg = (
                  f"{response} could not be interpreted as a valid " +
                  "duration or end time.")
                io_utils.print_status(
                  "Error", msg, line_length=wl_obj.line_length)
            # end if
        # Set the entry's duration.
        entry.duration = duration
        return 1
    except Exception as err:
        _z_exc("wl_add.py/add_duration", err)
    # end try
# end function


def add_note(wl_obj, entry, edit=False):
    """-----------------------------------------------------------------
        Allows the user to add a note for a task.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Keyword Arguments:
        - edit -- edit an existing entry (default False)

        Returns:  0 if the user chooses to abort, -1 if the user chooses
         to go back; otherwise 1.
       -----------------------------------------------------------------
    """
    try:
        # Refresh the entry's attributes.
        if edit:
            _screen_reset_edit(wl_obj, entry)
        else:
            _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
        # end if
        # Print the appropriate help text.
        wl_obj.help.print_help(
          wl_obj.show_help, "Task Notes", "_ah_note",
          line_length=wl_obj.line_length)
        # Print navigational instructions.
        if not edit:
            wl_resource.print_nav(q=True, b=True)
        # end if
        # Build prompt.
        if edit:
            prompt = (
              "Please enter a new note for this task, or press [ENTER] to " +
              "leave the note unchanged.")
        else:
            prompt = (
              "Please enter a note for this task, or press [ENTER] to " +
              "continue.")
        # end if
        # Print the prompt and get the response.
        response = io_utils.get_input(prompt, must_respond=False)
        # If editing and the user didn't enter anything, return.
        if edit and response == "":
            return 0
        # end if
        # The following are only valid if the entry is being created,
        #  not edited:
        if not edit:
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0
            # If the user chose to go back, also exit.
            elif re.match(r"-b", response, re.I):
                return -1
            # end if
        # end if
        # If the user chose to toggle help, do that.
        if re.match(r"-h", response, re.I):
            wl_obj.show_help = not(wl_obj.show_help)
        # If the user entered something else, set the notes attribute.
        elif response:
            entry.notes = response
        # end if
        return 1
    except Exception as err:
        _z_exc("wl_add.py/add_note", err)
    # end try
# end function


def add_recurrance(wl_obj, entry):
    """-----------------------------------------------------------------
        Asks the user if he/she wants the task to be recurring, and if
         yes, determines the recurrance dates.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Returns:  1 if successful, 0 if the user chooses to abort, or
         -1 if the user chooses to go back.  If the user wants the task
         to be recurring, a list of entry objects.
       -----------------------------------------------------------------
    """
    try:
        # Run in a loop until a valid response is obtained (function
        #  exits immediately then).
        while True:
            # Refresh the entry's attributes.
            _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # Print the appropriate help text.
            wl_obj.help.print_help(
              wl_obj.show_help, "Task Recurrance", "_ah_recurrance1",
              line_length=wl_obj.line_length)
            # Print navigational instructions.
            wl_resource.print_nav(q=True, b=True)
            # Print the prompt and get the response.  (Don't use the
            #  yes_no function because the user can also toggle help or
            #  exit/go back here.)
            response = io_utils.get_input(
              "Do you want this task to be recurring? [Y/N]:")
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0, []
            # If the user chose to go back, also exit.
            elif re.match(r"-b", response, re.I):
                return -1, []
            # If the user chose to toggle help, do that.
            elif re.match(r"-h", response, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user chose No, set the attribute and return.
            elif response[0].lower() == "n":
                entry.recurring = False
                return 1, []
            # If the user chose Yes, set the attribute and go the
            #  function that determines recurrances.
            elif response[0].lower() == "y":
                entry.recurring = True
                rec_list = _find_recurrances(wl_obj, entry)
                # If recurrances were successfully determined, return
                #  the list of entries.
                if rec_list:
                    return 1, rec_list
                # If the user decided not to set recurrances, reset the
                #  attributes and return.
                else:
                    entry.recurring = False
                    for key in entry.rec_interval:
                        entry.rec_interval[key] = None
                    # end for
                    return 1, []
                # end if
            # Otherwise print an error message and try again.
            else:
                io_utils.print_status(
                  "Error", f"{response} was not a valid response.",
                  line_length=wl_obj.line_length)
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_add.py/add_recurrance", err)
    # end try
# end function


def add_time(wl_obj, entry, edit=False):
    """-----------------------------------------------------------------
        Gets the user's input for a task time, then sets the log entry's
         attribute.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Keyword Arguments:
        - edit -- edit an existing entry (default False)

        Returns:  1 if successful, 0 if the user chooses to abort, or
         -1 if the user chooses to go back.
       -----------------------------------------------------------------
    """
    try:
        # Run in a loop until a valid time is obtained.
        valid = False
        while not valid:
            # Refresh the entry's attributes.
            if edit:
                _screen_reset_edit(wl_obj, entry)
            else:
                _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # end if
            # Print the appropriate help text.
            wl_obj.help.print_help(
              wl_obj.show_help, "Task Time", "_ah_time",
              line_length=wl_obj.line_length)
            # Print navigational instructions.
            if not edit:
                wl_resource.print_nav(q=True, b=True)
            # end if
            # Build prompt.
            if edit:
                prompt = (
                  "Please enter a new start time for this task, or press " +
                  "[ENTER] to leave the start time unchanged:")
            else:
                prompt = "Please enter the start time for this task:"
            # end if
            # Print the prompt and get the response.
            response = io_utils.get_input(prompt, must_respond=False)
            # If editing and the user didn't enter anything, return.
            if edit and response == "":
                return 0
            # end if
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0
            # If the user chose to go back, also exit.
            elif re.match(r"-b", response, re.I):
                return -1
            # If the user chose to toggle help, do that.
            elif re.match(r"-h", response, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user didn't enter anything (and isn't editing),
            #  show an error message and loop back.
            elif response == "":
                io_utils.print_status(
                  "Error", "You did not enter anything.",
                  line_length=wl_obj.line_length)
                continue
            # end if
            # Otherwise parse the string to determine the time.
            else:
                entry_time = wl_datetime.parse_time_input(wl_obj, response)
            # end if
            if entry_time:
                valid = True
            else:
                msg = f"{response} could not be interpreted as a valid time."
                io_utils.print_status(
                  "Error", msg, line_length=wl_obj.line_length)
            # end if
        # Set the entry's start time.
        entry.time = entry_time
        return 1
    except Exception as err:
        _z_exc("wl_add.py/add_time", err)
    # end try
# end function


def add_title(wl_obj, entry, edit=False):
    """-----------------------------------------------------------------
        Gets the user's input for a task title, then sets the log
         entry's attribute.

        Arguments:
        - wl_obj -- the work log object
        - entry -- the log entry object

        Keyword Arguments:
        - edit -- edit an existing entry (default False)

        Returns:  1 if successful, or 0 if the user chooses to abort.
       -----------------------------------------------------------------
    """
    try:
        # Run in a loop until a valid title is obtained.
        valid = False
        while not valid:
            # Refresh the entry's attributes.
            if edit:
                _screen_reset_edit(wl_obj, entry)
            else:
                _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # end if
            # Print the appropriate help text.
            wl_obj.help.print_help(
              wl_obj.show_help, "Task Title", "_ah_title",
              line_length=wl_obj.line_length)
            # Print navigational instructions.
            if not edit:
                wl_resource.print_nav(q=True, b=False)
            # end if
            # Build prompt.
            if edit:
                prompt = (
                  "Please enter a new title for this task, or press " +
                  "[ENTER] to leave the title unchanged:")
            else:
                prompt = "Please enter the title for this task:"
            # end if
            # Print the prompt and get the response.
            response = io_utils.get_input(prompt, must_respond=False)
            # If editing and the user didn't enter anything, return.
            if edit and response == "":
                return 0
            # end if
            # If the user chose to abort, exit immediately.
            if re.match(r"-q", response, re.I):
                return 0
            # If the user chose to toggle help, do that.
            elif re.match(r"-h", response, re.I):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # If the user chose to toggle help, do that.
            elif (
              (wl_obj.show_help is True and response.lower() == "-help off") or
              (wl_obj.show_help is False and response.lower() == "-help on")):
                wl_obj.show_help = not(wl_obj.show_help)
                continue
            # The task title can be any string, as long as it's not
            #  empty.
            elif response != "":
                # Set the attribute and exit the loop.
                entry.title = response
                valid = True
            else:
                # Print the error message and prompt to try again.
                io_utils.print_status(
                  "Error", "You did not enter anything.",
                  line_length=wl_obj.line_length)
            # end if
        # end while
        return 1
    except Exception as err:
        _z_exc("wl_add.py/add_title", err)
    # end try
# end function


def _find_recurrances(wl_obj, entry):
    """-----------------------------------------------------------------
        Prompts the user to set the frequency and range of a task's
         recurrance.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.

        Returns:  A list of entry objects, or an empty list if the user
         aborts the process.
       -----------------------------------------------------------------
    """
    try:
        # Loop until user aborts or a valid recurrance is set.
        valid = False
        while not valid:
            # Reset the screen.
            _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
            # See if the user wants a regular occurrance.
            io_utils.print_block(wl_obj.help.help_list["_ah_recurrance2"])
            response = io_utils.menu(
              ["Daily", "Weekly", "Monthly", "Other"], keystroke_list="#",
              line_length=wl_obj.line_length)
            # If the user chose to quit, confirm before quitting.
            if response == 0:
                confirm = io_utils.yes_no(
                  "Are you sure you want make this task non-recurring?",
                  line_length=wl_obj.line_length)
                if confirm:
                    wl_obj.recurring = False
                    return []
                else:
                    continue
                # end if
            # Regular daily, weekly or monthly recurrance.
            elif response < 4:
                # Reset the screen and then get the recurrance dates.
                _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
                # Set the rec_interval attribute.
                entry.rec_interval["unit"] = response
                return _set_occurrances(wl_obj, entry)
            # Irregular recurrance.
            else:
                io_utils.print_block(wl_obj.help.help_list["_ah_recurrance3"])
                day_int = io_utils.menu(
                  ["One or more specific days of the week.",
                   "One or more specific days of the month."],
                  keystroke_list="#", line_length=wl_obj.line_length)
                if day_int == 0:
                    confirm = io_utils.yes_no(
                      "Are you sure you want make this task non-recurring?",
                      line_length=wl_obj.line_length)
                    if confirm:
                        wl_obj.recurring = False
                        return []
                    else:
                        continue
                    # end if
                # Code for weekday recurrance.
                elif day_int == 1:
                    # Set the interval for weekly.
                    entry.rec_interval["unit"] = 2
                    # First select the weekday(s).
                    prompt = (
                      "Select the day(s) that you want this task to recur:")
                    days = io_utils.menu(
                      wl_resource.days[1:], keystroke_list="#", multiple=True,
                      prompt=prompt, line_length=wl_obj.line_length)
                    # If the user aborts, loop back.
                    if days == 0:
                        continue
                    # end if
                    day_list = []
                    for day in days:
                        day_list.append(wl_resource.days[day])
                    # end for
                    day_list = str_utils.comma_str_from_list(day_list)
                    prompt = (
                      f"Do you want this task to recur every {day_list} or " +
                      "less often?")
                    opt_list = [
                      f"Every {day_list}", f"Every other {day_list}",
                      f"Every third {day_list}", "Less often"]
                    skip = io_utils.menu(
                      opt_list, keystroke_list="#", prompt=prompt,
                      line_length=wl_obj.line_length)
                    if skip == 0:
                        continue
                    elif skip == 4:
                        prompt = (
                          "Enter how often you want the task to recur.  " +
                          "For example, enter [4] if you want the task to " +
                          f"recur every fourth {day_list}.  The maximum " +
                          "interval between recurrances is 30 weeks.")
                        good = False
                        while not good:
                            skip = io_utils.get_input(prompt, typ=int)
                            if not (0 <= skip < 31):
                                msg = (
                                  "Sorry, the number of weeks between " +
                                  "recurrances must be between 1 and 30.")
                                io_utils.print_status(
                                  "Error", msg,
                                  line_length=wl_obj.line_length)
                            else:
                                good = True
                            # end if
                        # end while
                        if skip == 0:
                            continue
                        # end if
                    # end if
                    # Reset the screen and return the occurances.
                    _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
                    # Set the other rec_interval attributes.
                    entry.rec_interval["days"] = days
                    entry.rec_interval["skip"] = skip
                    # Return the occurances.
                    return _set_occurrances(wl_obj, entry)
                # Code for monthly recurrance.
                else:
                    entry.rec_interval["unit"] = 3
                    # First determine the type of recurrance.
                    choice = io_utils.menu(
                      ["Specific dates during the month (3rd, 15th, etc.)",
                       "Specific days during the month (2nd Saturday, etc.)"],
                      keystroke_list="#",
                      prompt="Select when you want the task to recur:",
                      line_length=wl_obj.line_length)
                    # 0 = quit.
                    if choice == 0:
                        continue
                    # 1 = dates.
                    elif choice == 1:
                        wl_obj.help.print_help(
                          wl_obj.show_help, "Task Recurrance - By Date",
                          "_ah_recurrance4", line_length=wl_obj.line_length)
                        # Farm out getting a list of dates to a helper
                        #  function.
                        dates = _get_dates(wl_obj)
                        # If the user chose not to enter any dates, loop
                        #  back to the begining.
                        if not dates:
                            continue
                        # end if
                        # Reset the screen.
                        _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
                        # Set the rec_interval attribute.
                        entry.rec_interval["dates"] = dates
                        return _set_occurrances(wl_obj, entry)
                    # 2 == days.
                    else:
                        # First select the weekday(s).
                        prompt = (
                          "Select the day(s) that you want this task to " +
                          "recur")
                        days = io_utils.menu(
                          wl_resource.days[1:], keystroke_list="#",
                          multiple=True, prompt=prompt,
                          line_length=wl_obj.line_length)
                        # If the user aborts, loop back.
                        if days == 0:
                            continue
                        # end if
                        day_list = []
                        for day in days:
                            day_list.append(wl_resource.days[day])
                        # end for
                        day_list = str_utils.comma_str_from_list(day_list)
                        # Then select the weeks.
                        prompt = (
                          f"Select the {day_list} on which you want the" +
                          "task to recur, separating multiple entries with" +
                          "commas.")
                        opt_list = [
                          f"The first {day_list}", f"The second {day_list}",
                          f"The third {day_list}", f"The fourth {day_list}",
                          f"The fifth {day_list}"]
                        ordinal = io_utils.menu(
                          opt_list, keystroke_list="#", multiple=True,
                          line_length=wl_obj.line_length)
                        # If the user chose to abort, loop back.
                        if ordinal == 0:
                            continue
                        # end if
                        # Reset the screen.
                        _screen_reset(wl_obj, entry, wl_obj.total_entries + 1)
                        # Set the rec_interval attribute.
                        entry.rec_interval["days"] = days
                        entry.rec_interval["ordinal"] = ordinal
                        # Return the occurances.
                        return _set_occurrances(wl_obj, entry)
                    # end if
                # end if
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_add.py/_find_recurrances", err)
    # end try
# end function


def _get_dates(wl_obj):
    """-----------------------------------------------------------------
        Gets a list of integers representing dates from the user.

        Arguments:
        - wl_obj -- the work log object

        Returns:  A list of integers representing dates, or an empty
         list if the user enters nothing.
       -----------------------------------------------------------------
    """
    try:
        # Loop.
        valid = False
        while not valid:
            # Get a response from the user (string)
            response = io_utils.get_input("Enter one or more dates:")
            dates = re.findall(r"-?\d+", response)
            # If the user didn't enter any dates, ask to retry or quit.
            if len(dates) == 0:
                io_utils.print_status(
                  "Error", "You did not any recognizable dates.",
                  line_length=wl_obj.line_length)
                if io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    continue
                else:
                    return []
                # end if
            # end if
            # Use a set to create an ordered list of non-duplicate
            #  dates.
            date_set = set()
            for date in dates:
                if -31 <= int(date) <= 31:
                    date_set.add(int(date))
                # end if
            # end for
            dates = list(date_set)
            dates.sort()
            if len(dates) == 0:
                io_utils.print_status(
                  "Error", msg="You did not any recognizable dates.",
                  line_length=wl_obj.line_length)
                if io_utils.yes_no(
                  "Try again?", line_length=wl_obj.line_length):
                    continue
                else:
                    return []
                # end if
            # end if
            valid = True
        # end while
        return dates
    except Exception as err:
        _z_exc("wl_add.py/_get_dates", err)
    # end try
# end function


def _screen_reset(wl_obj, entry, entry_number):
    """-----------------------------------------------------------------
        Internal function which refreshes the screen with a log entry's
         attributes.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.
        - entry_number -- the number of the current entry.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen and print the program header.
        wl_resource.print_header(wl_obj)
        # Display the entry number.
        print(f"Entry #{entry_number}", ":\n")
        # Loop through the entry object's attributes.
        for attr, value in entry.__dict__.items():
            # Display only those attributes that are editable, and have
            #  been entered.
            if (
              (value is not None) and
              (attr not in ["id", "info", "rec_interval"])):
                print(
                  f"{attr.title()}:  " +
                  f"{wl_resource.format_string(wl_obj, value)}")
            # end if
        # end for
        # Blank line.
        print()
        return
    except Exception as err:
        _z_exc("wl_add.py/_screen_reset", err)
    # end try
# end function


def _screen_reset_edit(wl_obj, entry):
    """-----------------------------------------------------------------
        Internal function which refreshes the screen with an existing
         log entry's attributes, and proposed edits.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen and print the program header.
        wl_resource.print_header(wl_obj)
        # Display the entry number.
        print(f"Editing {entry.info['ndx']}…")
        # Loop through the entry object's attributes.
        for attr, value in entry.__dict__.items():
            # Print only those attributes that are editable.
            if (attr in ["title", "date", "time", "duration", "notes"]):
                # Print the original value.
                print(
                  f"{attr.title()}:  "
                  f"{wl_resource.format_string(wl_obj, entry.info[attr])}",
                  end="")
                # If the value has changed, print it as well.
                if value != entry.info[attr]:
                    print(
                      f" -> {wl_resource.format_string(wl_obj, value)}")
                else:
                    print()
                # end if
            # end if
        # end for
        # Blank line.
        print()
        return
    except Exception as err:
        _z_exc("wl_add.py/_screen_reset_edit", err)
    # end try
# end function


def _set_occurrances(wl_obj, entry):
    """-----------------------------------------------------------------
        Obtains an end date for a recurring task, and calculates the
         specific dates for the task.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object.

        Returns:  a list of dates if successful, else an empty list.
       -----------------------------------------------------------------
    """
    try:
        recurrance_list = []
        # The recurrance pattern is governed by five flags:
        # * unit:  This is the base unit; daily, weekly, or monthly.
        # * skip:  This denotes how often to skip the base unit.  For
        #    example, if a task is flagged to recur on Tuesdays, a value
        #    of [2] for skip would change the recurrance to every other
        #    Tuesday.
        # * days:  Only relevant if unit is weekly or monthly.  Day(s)
        #    of the week for the task to recur.  Can be from [1]
        #    (Sunday) to [7] (Saturday).  This value always needs to be
        #    converted to and from Python's Monday-based week.
        # * ordl:  Only relevant if unit is monthly and days of the week
        #    are specified; indicates on which weekdays the task should
        #    recur.  For example, if days is Tuesday, [1, 3] for ordl
        #    indicates the first and third Tuesdays of each month.
        # * dates:  Only relevant if unit is monthly; denotes days of
        #    the month that the task should recur.  Can be from [1] to
        #    [31] for absolute dates, and from [-1] to [-31] for dates
        #    relative to the end of the month; dates before the first
        #    day or after the last day of any particular month are
        #    ignored.
        #
        # The screen should have been reset just prior to the calling of
        #  this function.  Print the string representation of the
        #  recurrance interval.
        print(wl_resource.format_recurrance_pattern(wl_obj, entry))
        # Run this part inside a loop, in case the user doesn't like the
        #  results and wants to try a different end date.
        good = False
        while not good:
            # Ask the user for an end date.
            valid = False
            while not valid:
                end_date = io_utils.get_input(
                  "Please enter the last date for this task:")
                end_date = wl_datetime.parse_date_input(wl_obj, end_date)
                if not end_date:
                    io_utils.print_status(
                      "Error", "You did not enter a valid last date.",
                      line_length=wl_obj.line_length)
                    go = io_utils.yes_no(
                      "Do you want to try again?",
                      line_length=wl_obj.line_length)
                    if not go:
                        return []
                    else:
                        continue
                    # end if
                elif end_date <= entry.date:
                    print(
                      "The last date must be after the date of the original " +
                      "task.")
                    go = io_utils.yes_no(
                      "Do you want to try again?",
                      line_length=wl_obj.line_length)
                    if not go:
                        return []
                    else:
                        continue
                    # end if
                else:
                    valid = True
                # end if
            # end while
            # Calculate for daily options.
            if entry.rec_interval["unit"] == DAILY:
                # This is the simplest calculation.  Just skip the
                #  appropriate number of days per occurrance.
                # Use the skip argument to create a timedelta object.
                interval = datetime.timedelta(days=entry.rec_interval["skip"])
                # Now start creating dates, starting from the date of
                #  the first occurrance.
                cur_date = entry.date + interval
                while cur_date <= end_date:
                    recurrance_list.append(cur_date)
                    cur_date += interval
                # end while
            # Calculate for weekly options.
            elif entry.rec_interval["unit"] == WEEKLY:
                # Weekly recurrances are a combination of days and
                #  (optionally) a skip value.  The skip value determines
                #  the interval between recurrances.
                interval = 7 * entry.rec_interval["skip"]
                # Identify the weekday of the original task (but note
                #  that the task does not necessarily need to recur on
                #  this day).
                cur_date = []
                start_day = wl_datetime.conv_wkday(entry.date.weekday())
                for day in entry.rec_interval["days"]:
                    if day == start_day:
                        cur_date.append(
                          entry.date + datetime.timedelta(days=interval))
                    elif day > start_day:
                        cur_date.append(
                          entry.date +
                          datetime.timedelta(days=(day - start_day)))
                    else:
                        cur_date.append(
                          entry.date +
                          datetime.timedelta(
                            days=(day - start_day + interval)))
                    # end if
                # end for
                # Make sure the recurrances get made in order.
                cur_date.sort()
                # Now start setting dates.
                # If the end date is before the first recurrance, don't
                #  do anything.
                if not(end_date < cur_date[0]):
                    # Loop.
                    done = False
                    while not done:
                        # Loop through the recurrances.  The first one
                        #  to be after the end date breaks the loop.
                        for d in range(len(cur_date)):
                            if cur_date[d] <= end_date:
                                recurrance_list.append(cur_date[d])
                                cur_date[d] += (
                                  datetime.timedelta(days=interval))
                            else:
                                done = True
                                break
                            # end if
                        # end for
                    # end while
                # end if
            # Calculate for monthly options.
            else:
                # Monthly recurrances can be more complicated.  They can
                #  occur on specific dates of the month, or specific
                #  weekdays.  The latter is more complex because the
                #  date(s) that the specific weekday(s) fall upon must
                #  be recalculated for each month.
                month = entry.date.month
                year = entry.date.year
                # First calculate for specific dates during the month.
                if entry.rec_interval["dates"]:
                    done = False
                    while not done:
                        # If any of the dates are negative (counting
                        #  backwards from the end of the month), they
                        #  need to be converted to positive dates for
                        #  each new month.  (The original dates need to
                        #  be stored and restored at the end of the
                        #  loop, so they can be correctly converted for
                        #  the next month.)
                        orig_dates = list(entry.rec_interval["dates"])
                        for d in range(len(entry.rec_interval["dates"])):
                            if entry.rec_interval["dates"][d] < 0:
                                # Need to offset plus one because -1
                                #  represents the last day of the month.
                                entry.rec_interval["dates"][d] = (
                                  wl_datetime.last_date(month, year) +
                                  entry.rec_interval["dates"][d] + 1)
                            # end if
                        # end for
                        # Now resort the list.
                        entry.rec_interval["dates"].sort()
                        # Loop through the dates for recurrance.
                        for date in entry.rec_interval["dates"]:
                            # Ignore any numbers that are still
                            #  negative.
                            if date > 0:
                                # The first recurrance to extend beyond
                                #  the end date breaks the loop.
                                try:
                                    cur_date = datetime.date(year, month, date)
                                    if entry.date < cur_date <= end_date:
                                        recurrance_list.append(cur_date)
                                    else:
                                        if cur_date > end_date:
                                            done = True
                                            break
                                        # end if
                                    # end if
                                except ValueError:
                                    pass
                                # end try
                            # end if
                        # end for
                        # Increment the month.
                        month += 1
                        if month == 13:
                            month = 1
                            year += 1
                        # end if
                        # Restore the unaltered date list.
                        entry.rec_interval["dates"] = list(orig_dates)
                    # end while
                # Calculate for specific weekdays during the month.
                elif entry.rec_interval["days"]:
                    done = False
                    while not done:
                        # Both ordl and days can have multiple values;
                        #  ordl is the outside loop.
                        for ordl in entry.rec_interval["ordinal"]:
                            brk = False
                            # Loop through each weekday
                            for day in entry.rec_interval["days"]:
                                cur_date = wl_datetime.find_weekday(
                                  day, ordl, month, year)
                                # If the function returns None, it means
                                #  that that particular combination (for
                                #  example, the fifth Friday) fell
                                #  outside the month's range.  Bypass
                                #  that date.
                                if cur_date:
                                    if cur_date > entry.date:
                                        if cur_date <= end_date:
                                            recurrance_list.append(cur_date)
                                        else:
                                            # If past the end date,
                                            #  break all three loops.
                                            brk = True
                                            done = True
                                            break
                                        # end if
                                    # end if
                                # end if
                            # end for
                            if brk:
                                break
                            # end if
                        # end for
                        # Once all the occurances for the month are set,
                        #  go on to the next month.
                        month += 1
                        if month > 12:
                            month == 1
                            year += 1
                        # end if
                    # end while
                # end if
            # end if
            # Some occurances may be out of order; sort the list.
            recurrance_list.sort()
            # Now display the results.
            if len(recurrance_list) == 1:
                t = "time"
            else:
                t = "times"
            print(
              f"This task will recur {len(recurrance_list)} {t} between ",
              f"{wl_datetime.dformat(entry.date, wl_obj.date_format)} and ",
              f"{wl_datetime.dformat(end_date, wl_obj.date_format)}:", "\n")
            # Print the recurrance dates, three across.
            for n in range(len(recurrance_list)):
                print(
                  wl_datetime.dformat(recurrance_list[n], wl_obj.date_format),
                  end=" " * 10)
                if n % 3 == 2:
                    print()
                # end if
            # end for
            go = io_utils.yes_no("Proceed?", line_length=wl_obj.line_length)
            if go:
                # Set the rec_interval attribute.
                entry.rec_interval["end"] = end_date
                good = True
            else:
                action = io_utils.menu(
                  ["Select a different end date.",
                   "Cancel making this task recurring."], keystroke_list="#",
                  prompt="What would you like to do?", quit_=False,
                  line_length=wl_obj.line_length)
                if action == 2:
                    return []
                # end if
            # end if
        # end while
        return recurrance_list
    except Exception as err:
        _z_exc("wl_add.py/_set_recurrances", err)
    # end try
# end function
