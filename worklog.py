"""
    Contains the specification for the WorkLog object.

    Class Definitions:
    - WorkLog -- the work log object.

    Private Functions:
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
    print("An interal error occurred in " + loc, err)
    sys.exit(
      "Please report the above error and the circumstances which caused it " +
      "to the developer.")
    return
# end function


# Other imports.
try:
    import datetime

    import io_utils
    import logentry
    import wl_add
    import wl_datetime
    import wl_help
    import wl_manual
    import wl_resource
    import wl_search
except Exception as err:
    _z_exc("worklog.py/module imports", err)
# end try


# Constants.
TITLE_SORT = 0
DATE_SORT = 1
QUIT = 0
DATE_F = 1
TIME_F = 2


class WorkLog:
    """
        Object containing one or more task entries.

        Attributes:
        - entries -- a list of individual entries, each of which is a
           LogEntry object.
        - total_entries -- the total number of entries.
        - action -- flag which contains the current action to take.
        - show_help -- flag indicating whether or not to display help
           text.
        - line_length -- the width of the screen in characters.
        - changed -- flag indicating whether or not any entries in the
           log have changed.
        - filename -- the external filename that the data for the log
           is read from and written to.
        - last_modified -- the datetime that the log file was last
           saved.
        - date_format -- the user's preferred date format.
        - time_format -- the user's preferred time format.
        - sorts -- two lists, containing the IDs of all entries sorted
           by name, and by datetime.
        - info -- a dictionary, usually empty, containing information
           about the WorkLog object to be written to a file.
        - help -- a WlHelp object, containing methods for displaying
           help text.

        Public Methods:
        - action_get -- asks for and gets an action from the user.
        - action_take -- takes the action the user specifies.

        Private Methods:
        - _add_entry -- adds a single entry to the work log object.
        - _add_recurring_entries -- adds a series of recurring entries
           to the work log object.
        - _do_add -- creates a new LogEntry object, initializes it with
           input from the user, and adds it to the work log object.
        - _do_add_recurring_entries -- if the user has indicated that
           he/she wants a task to recur at certain intervals, creates
           the recurring entries and adds them to the WorkLog object.
        - _do_close -- closes the file that the work log object is
           associated with; if the WorkLog object has changed, prompts
           the user to save the file.
        - _do_create -- creates a new file for a new work log object; if
           the file exists, prompts the user to open or overwrite that
           file, or to enter a different filename.
        - _do_lookup -- searches for entries based on the user's input;
           allows the user to edit or delete entries that are found.
        - _do_open -- opens a file and populates the work log object
           with its data.
        - _do_save -- saves the data in the WorkLog object to a file.
        - _do_sort -- updates the work log object's sorted lists when a
           new entry is added.
        - _init_entries -- initializes log entries from data read from
           a file, and adds the entries to the work log object.
        - _init_worklog -- initializes the work log object from data
           read from a file.

        Magic Methods:
        - __init__ -- creates a new WorkLog object.
        - __eq__ -- overrides the = operator to compare objects.
       -----------------------------------------------------------------
    """

    def __init__(self):
        """
            Returns an empty log object.

            Sets the total_entries attribute to -1 as a flag that the
             object is unitialized.
           -------------------------------------------------------------
        """
        # Set defaults.
        self.entries = []
        self.total_entries = -1
        self.action = None
        self.show_help = None
        self.line_length = None
        self.changed = False
        self.filename = ""
        self.last_modified = None
        self.date_format = None
        self.time_format = None
        self.sorts = [[], []]
        self.info = {}
        self.help = wl_help.WlHelp()
    # end method

    def __eq__(self, other):
        """
            Overrides the equality operator.

            Allows work log objects to be compared with "=".
           -------------------------------------------------------------
        """
        return self.__dict__ == other.__dict__
    # end method

    def action_get(self):
        """
            Gets an action from the user.

            If the log object is unitialized, asks the user to open or
             create a file.

            Arguments:  none.

            Returns:  False if the user chooses to exit the program,
             else True.
           -------------------------------------------------------------
        """
        try:
            print()
            # If the total_entries attribute is -1, the object is not
            #  initialized.  Ask the user to open or create a log file.
            if self.total_entries == -1:
                keystroke_list = ["O", "N", "X", "M"]
                action = io_utils.menu(
                  ["Open Log File", "New Log File", "Change Settings",
                   "Read User Manual"],
                  option_type="actions", keystroke=True,
                  keystroke_list=keystroke_list, lines=True,
                  top_level=True, line_length=self.line_length)
                # If the user chooses to quit here...
                if action == 0:
                    # Set the action attribute so _action_take knows to
                    #  do nothing.
                    self.action = None
                    # return False to main() so it knows to exit the
                    #  program.
                    return False
                else:
                    # Set the action attribute, skip the other menu code and
                    #  immediately return.
                    self.action = keystroke_list[action - 1]
                    return True
                # end if
            # end if
            # If the object has been initialized, skip the above code,
            #  print the header and ask the user what they want to do.
            wl_resource.print_header(self)
            keystroke_list = ["A", "F", "S", "C", "X"]
            action = io_utils.menu(
              ["Add Entries", "Find/Edit/Delete Entries", "Save Log File",
               "Close Log File", "Change Settings"], option_type="actions",
              lines=True, keystroke=True, keystroke_list=keystroke_list,
              top_level=True, line_length=self.line_length)
            # If the user chose to quit...
            if action == QUIT:
                # Set the action attribute to None, which will be a flag
                #  for the action_take method.
                self.action = None
                # If the log object has changed, prompt to save.
                if self.changed is True:
                    save = io_utils.yes_no(
                      "The log file has changed.  Do you want to save it?",
                      line_length=self.line_length)
                    # If yes, just save the file now (bypass action_take
                    #  so that it will still exit).
                    if save:
                        self._do_save
                    # end if
                # end if
                # Return the flag to end the object loop.
                return False
            else:
                # Set the action attribute.
                self.action = keystroke_list[action - 1]
            # end if
            # Always return True unless the user chose to quit.
            return True
        except Exception as err:
            _z_exc("worklog.py/WorkLog/action_get", err)
        # end try
    # end method

    def action_take(self):
        """
            Takes the action specified by the user.

            Action is stored in the object's action attribute.  If the
            action attribute is set to None, the method immediately
            exits to the main menu.

            Arguments:  none.

            Returns:  True if the user wants to take another action;
             else False, which will break the loop and send the script
             back to the start.  Also False if the user quits.
            ------------------------------------------------------------
        """
        try:
            # Flag to the main function on whether or not to loop back
            #  to the beginning.
            # If the action attribute is None, user has quit.  Do
            #  nothing.  Return False to ensure that both the inner and
            #  outer loop stop.
            if self.action is None:
                return False
            # Take the action specified:
            # If the user chooses to open a file (at initalization)...
            elif self.action == "O":
                # Try to open and read in a file.  Return whether it
                #  succeeded or failed.  If it succeeded, go to the
                #  actions menu.  If it failed, go to the main menu.
                return self._do_open()
            # If the user chooses to create a file (at initialization)...
            elif self.action == "N":
                # Try to create a file.  Return whether it succeeded or
                #  failed.  If it succeeded, go to the actions menu.  If
                #  it failed, go to the main menu.
                return self._do_create()
            # If the user wants to add entries...
            elif self.action == "A":
                self._do_add()
            # If the user wants look up, copy, edit or delete entries...
            elif self.action == "F":
                self._do_lookup()
            # If the user wants to save the log file (but keep
            #  working)...
            elif self.action == "S":
                self._do_save()
            # If the user wants to close the file...
            elif self.action == "C":
                # Close the file and return to the main menu.
                return self._do_close()
            # If the user wants to access the settings menu...
            elif self.action == "X":
                self._do_settings(self.total_entries)
            # If the user wants to read the user manual...
            elif self.action == "M":
                input(wl_manual.string)
                io_utils.clear_screen
            # end if
            # To go back to the actions menu, return True.
            return True
        except Exception as err:
            _z_exc("worklog.py/WorkLog/action_take", err)
        # end try
    # end method

    def _do_add(self):
        """
            Adds one or more entry objects to the log object.

            Arguments:  none.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            # List of object attributes to set (easier than directly
            #  iterating through the attributes).
            attr_list = [
              "title", "date", "time", "duration", "notes", "recurring"]
            # Initialize list.
            recurring_entries = []
            # Like all of the _do methods, the entire method is inside a
            #  loop, allowing the user to add as many entries as they
            #  want.
            not_done = True
            while not_done:
                cancel = False
                # First, create a new log entry object.
                new_entry = logentry.LogEntry()
                # Go through the list and set values for each attribute.
                #  Because the user can choose to back up, we don't use
                #  a for loop to iterate through the attributes.
                attrib = 0
                # Loop runs until the last attribute is set.
                while attrib < len(attr_list):
                    # Get the attribute name.
                    attr = attr_list[attrib]
                    # The title attribute is the only one which does not
                    #  allow the user to go back (because it's the first
                    #  attribute set).
                    if attr == "title":
                        go = wl_add.add_title(self, new_entry)
                    # end if
                        # "date" must be convertible to a date object.
                    elif attr == "date":
                        go = wl_add.add_date(self, new_entry)
                        # If the user goes back a step, clear the
                        #  previous attribute.
                        if go == -1:
                            new_entry.title = None
                        # end if
                    # "time" must be convertible to a time object.
                    elif attr == "time":
                        go = wl_add.add_time(self, new_entry)
                        # If the user goes back a step...
                        if go == -1:
                            new_entry.date = None
                        # end if
                    # "duration" must be convertible to a timedelta
                    #  object.
                    elif attr == "duration":
                        go = wl_add.add_duration(self, new_entry)
                        # If the user goes back a step...
                        if go == -1:
                            new_entry.time = None
                        # end if
                    # "notes" can be any string, including empty.
                    elif attr == "notes":
                        go = wl_add.add_note(self, new_entry)
                        # If the user goes back a step...
                        if go == -1:
                            new_entry.duration = None
                        # end if
                    # "recurring" will either be True of False, and if
                    #  True will also return a list of recurrance date
                    #  objects.
                    elif attr == "recurring":
                        recurring_entries = []
                        go, recurring_entries = wl_add.add_recurrance(
                          self, new_entry)
                        # If the user goes back a step...
                        if go == -1:
                            new_entry.notes = None
                        # end if
                    # end if
                    if go == 0:
                        # Print that the entry was cancelled.
                        io_utils.print_status(
                          "Status",
                          "Addition of this task has been cancelled.",
                          line_length=self.line_length)
                        # If the user aborts and does not want to start
                        #  another task, return immediately.
                        if io_utils.yes_no(
                          "Do you want to add another task?",
                          line_length=self.line_length):
                            cancel = True
                            break
                        else:
                            return
                        # end if
                    else:
                        attrib += go
                    # end if
                # end while
                if not cancel:
                    not_done = self._add_entry(new_entry, recurring_entries)
                # end if
            # end while
            return
        except Exception as err:
            _z_exc("worklog.py/WorkLog/do_add", err)
        # end try
    # end method

    def _add_entry(self, entry, recurring_entries):
        """
            Adds one entry.

            Arguments:
            - entry -- the entry to add.
            - recurring_entries -- the list of recurring entries, if
               there are any.

            Returns:  True if the user wants to add another task, else
             False.
           -------------------------------------------------------------
        """
        try:
            # Set the datetime attribute.
            entry.datetime = wl_add.add_datetime(entry)
            # Add the entry to the work log.
            self._do_sort(entry)
            self.entries.append(entry)
            # Now add the recurring entries, if any.
            self._add_recurring_entries(entry, recurring_entries)
            # And update.
            self.total_entries = len(self.entries)
            # Note the log object has changed.
            self.changed = True
            # Build status message.
            if recurring_entries:
                msg = f"{len(recurring_entries) + 1} entries added."
            else:
                msg = "Entry added."
            # end if
            # Update the total entries attribute.
            self.total_entries = len(self.entries)
            # Print that the entry was added.
            io_utils.print_status(
              "Status", msg, line_length=self.line_length)
            # Finally, ask the user if they want to add another
            #  entry.  (Whether they are done will be the opposite
            #  of their answer.)
            return io_utils.yes_no(
              "Do you want to add another task?", line_length=self.line_length)
        except Exception as err:
            _z_exc("worklog.py/WorkLog/do_add", err)
        # end try
    # end method

    def _add_recurring_entries(self, entry, recurrance_list):
        """
            Adds a series of recurring entries.

            Arguments:
            - entry -- the original entry.
            - recurrance_list -- the list of recurring dates.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            # If there are no recurrances, just return.
            if not recurrance_list:
                return
            # end if
            # Finish setting the original entry's attribute.
            entry.rec_total = len(recurrance_list)
            for n, date in enumerate(recurrance_list):
                # Create a new entry object with the original entry's
                #  attributes.
                new_entry = logentry.LogEntry()
                new_entry.title = entry.title
                # Different date.
                new_entry.date = date
                new_entry.time = entry.time
                # Set new datetime attribute.
                new_entry.datetime = wl_add.add_datetime(new_entry)
                new_entry.duration = entry.duration
                new_entry.notes = entry.notes
                # Recurrance-specific attributes.
                new_entry.recurring = False
                new_entry.rec_child_seq = (n + 1, len(recurrance_list))
                new_entry.rec_parent = entry.id
                # Add the entry to the work log.
                self._do_sort(new_entry)
                self.entries.append(new_entry)
            # end for
            return
        except Exception as err:
            _z_exc("worklog.py/WorkLog/do_add_recurring_entries", err)
        # end try
    # end method

    def _do_close(self):
        """
            Closes the work log object.

            The object will be overwritten by a new instance, or
             destroyed upon program exit.

            Arguments:  none.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            if self.changed and io_utils.yes_no(
              f"{self.filename} has changed.  Do you want to save it?",
              line_length=self.line_length):
                if not self._do_save():
                    io_utils.print_status(
                      "Error", "Error saving file.",
                      line_length=self.line_length)
                # end if
            else:
                io_utils.print_status(
                  "Status", f"{self.filename} closed.",
                  line_length=self.line_length)
            return False
        except Exception as err:
            _z_exc("worklog.py/WorkLog/do_close", err)
        # end try
    # end method

    def _do_create(self):
        """
            Creates a new file to store data from the log object.

            If the user names an existing file, offers to open that
             file.

            Arguments:  none.

            Returns:  True if successful; False if there was an error or
             the user aborts the process.
           -------------------------------------------------------------
        """
        try:
            # Call the io_utils method to get a filename and create the file.
            self.filename, go_open = io_utils.file_create(filetype="csv")
            # If no filename was returned, the attempt was unsuccessful.
            #  Return False
            if self.filename == "":
                return False
            # If the open flag was set, call _do_open for the file.
            elif go_open:
                success = self._do_open()
                if success:
                    return True
                else:
                    return False
                # end if
            else:
                self.total_entries = 0
                # Print status.
                io_utils.print_status(
                  "Status", f"{self.filename} created.",
                  line_length=self.line_length)
                return True
            # end if
        except Exception as err:
            _z_exc("worklog.py/WorkLog/do_create", err)
        # end try
    # end method

    def _do_lookup(self):
        """
            Searches for and displays one or more log entries.

            Arguments:  none.

            Returns:  True if successful; False if the user aborted.
           -------------------------------------------------------------
        """
        try:
            # Clear the screen.
            wl_resource.print_header(self)
            # If there are no entries in the log, tell the user and then
            #  return.
            if len(self.entries) == 0:
                io_utils.print_status(
                  "Error", "There are no tasks in the log to search!",
                  line_length=self.line_length)
                return False
            # end if
            # Main menu.
            option_list = [
              "By Date/Time", "By Duration", "By Text Search", "By RE Pattern"]
            prompt = "Please select a method by which to find entries:"
            search_opt = io_utils.menu(
              option_list, keystroke_list="#", prompt=prompt,
              line_length=self.line_length)
            # If the user quits, just return.
            if search_opt == 0:
                return False
            # end if
            # Otherwise call the appropriate lookup function.
            if search_opt == 1:
                results = wl_search.search_by_date(self)
            elif search_opt == 2:
                results = wl_search.search_by_duration(self)
            elif search_opt == 3:
                results = wl_search.search_by_text(self)
            else:  # search_opt == 4
                results = wl_search.search_by_re(self)
            # end if
            # If the search was unsuccessful, just return.
            if not results:
                return True
            # end if
            # Call the appropriate browse function, which will call other
            #  functions if needed.
            if type(results[0]) == datetime.date:
                wl_search.select_date(self, results)
                return True
            else:
                wl_search.select_entry(self, results)
                return True
            # end if
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_do_lookup", err)
        # end try
    # end method

    def _do_open(self):
        """
            Opens a log file and reads data into the log object.

            Arguments:  none.

            Returns:  True if successful; False if there was an error.
           -------------------------------------------------------------
        """
        try:
            # If we don't have a filename, get one.
            if self.filename == "":
                self.filename = io_utils.get_filename_open(filetype="csv")
            # end if
            # If self.filename is still empty, the user chose to go
            #  back, so just return.
            if self.filename == "":
                return False
            # end if
            # Open and read the file.
            entry_dict = io_utils.file_read(self.filename, filetype="csv")
            # If the file didn't open properly, let the user know before
            #  returning.
            if not entry_dict:
                io_utils.print_status(
                  "Error", f"{self.filename} could not be opened.")
                return False
            # end if
            # Pop the first entry in the list of dictionaries that was
            #  read from the file and use it to initialize the work log
            #  object.  Return False if the operation fails.
            if not self._init_worklog(entry_dict.pop(0)):
                return False
            # end if
            # Initialize the log entry objects.
            failed = self._init_entries(entry_dict)
            # Once all the entries have been added, sort the lists.
            self.sorts[TITLE_SORT].sort()
            self.sorts[DATE_SORT].sort()
            # Print final status.
            msg = f"{self.filename} opened.  {len(self.entries)} entries read."
            if failed:
                msg += (
                  f"  {self.total_entries - len(self.entries)} entries " +
                  "not read.  The file may be corrupted.")
            elif self.total_entries != len(self.entries):
                msg += (
                  f"  {self.total_entries} entries expected.  The file may " +
                  "have been edited outside the Work Log program.")
            io_utils.print_status(
              "Status", msg, line_length=self.line_length)
            # Finally reset the total_entries attribute to the actual
            #  number of entries added.
            self.total_entries = len(self.entries)
            return True
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_do_open", err)
        # end try
    # end method

    def _do_save(self):
        """
            Saves the log file.

            Allows the user to continue working with the log object.

            Arguments:  none.

            Returns:  True if successful; False if there was an error.
           -------------------------------------------------------------
        """
        try:
            self.last_modified = datetime.datetime.now()
            # Initialize a temporary list to hold the log data.
            entry_list = []
            # Create a dummy entry object, which will hold data for the
            #  log object.
            new_entry = logentry.LogEntry()
            fn = new_entry.FIELDNAMES
            new_entry.info = {
              "total_entries": self.total_entries,
              "date_format": self.date_format,
              "time_format": self.time_format, "show_help": self.show_help,
              "last_modified": self.last_modified}
            # Start the list with the dummy entry object.
            entry_dict = new_entry.to_dict()
            entry_list.append(entry_dict)
            # Now add all of the entries.
            for entry in self.entries:
                # For each entry object, convert to a dictionary.
                entry_dict = entry.to_dict()
                entry_list.append(entry_dict)
            # end for
            # Pass everything to the io_utils function.
            success = io_utils.file_write(
              self.filename, "csv", entry_list, fieldnames=fn)
            if success:
                # Print status.
                io_utils.print_status(
                  "status", f"{self.filename} saved.",
                  line_length=self.line_length)
                self.changed = False
                return True
            else:
                return False
            # end if
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_do_save", err)
        # end try
    # end method

    def _do_settings(self, flag):
        """
            Allows the user to change a setting.

            The date format, time format, or width of the screen can be
             changed.

            Arguments:  none.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            # Loop until the user is done.
            while True:
                # Clear screen and print header.
                wl_resource.print_header(self)
                # Print instructions.
                self.help.print_help(
                  self.show_help, "Settings", "_xh_settings",
                  line_length=self.line_length)
                # Show menu and get a response.
                response = io_utils.menu(
                  ["Set Date Format", "Set Time Format", "Set Screen Width"],
                  keystroke_list="#", help_toggle=True,
                  line_length=self.line_length)
                # If the user chose to toggle help, do that and then
                #  loop back.
                if str(response).lower() == "-h":
                    self.show_help = not self.show_help
                    continue
                # end if
                # If the user chose to go back, just return.
                if response == QUIT:
                    self.total_entries = flag
                    return
                # Otherwise, to change a setting, call the appropriate
                #  function.
                elif response == DATE_F:
                    wl_datetime.set_endian(self)
                elif response == TIME_F:
                    wl_datetime.set_time_format(self)
                else:  # response == 3
                    wl_resource.set_screen_width(self)
                # end if
            # end while
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_do_settings", err)
        # end try
    # end method

    def _do_sort(self, entry, update=False):
        """
            Maintains and updates the sort indexes for tasks.

            Arguments:
            - entry -- an entry to add or update.

            Keyword arguments:
            - update -- the update flag (default False).

            Returns:  nothing.
            ------------------------------------------------------------
        """
        try:
            # The log object maintains two sort indexes of its entries:
            #  by title and by datetime.  Two sorted lists are stored in
            #  the log object's sorts attribute.  Each list consists of
            #  a series of tuples, containing the key to be sorted, the
            #  title or date/time, and the ID of the associated entry.
            #
            # Create sort tuples for the entry.
            title_sort_item = (entry.title, entry.datetime, entry.id)
            date_sort_item = (entry.datetime, entry.title, entry.id)
            # Do this first if updating an entry.
            if update:
                # Find the original entry and delete it from both lists.
                for ndx, ent in self.sorts[TITLE_SORT]:
                    if ent[2] == entry.id:
                        del self.sorts[TITLE_SORT][ndx]
                        break
                    # end if
                # end for
                for ndx, ent in self.sorts[DATE_SORT]:
                    if ent[2] == entry.id:
                        del self.sorts[DATE_SORT][ndx]
                        break
                    # end if
                # end for
            # end if
            # Do this when adding/updating an entry.
            # Append the entry and sort the lists.
            self.sorts[TITLE_SORT].append(title_sort_item)
            self.sorts[TITLE_SORT].sort()
            self.sorts[DATE_SORT].append(date_sort_item)
            self.sorts[DATE_SORT].sort()
            return
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_do_sort", err)
        # end try
    # end method

    def _init_entries(self, entry_list):
        """
            Initializes a set of log entries.

            Takes a list of dictionaries which have been read from a
             data file, uses them to initialize log entry objects and
             adds the log entry objects to the work log object.

            Arguments:
            - entry_list -- the list of OrderedDicts holding the log
               entries.

            Returns:  the number of entries that could not be created.
           -------------------------------------------------------------
        """
        try:
            failed = 0
            # Iterate through the list of entry dictionaries.
            for x, entry in enumerate(entry_list):
                # Try to intialize the entry.
                if not self._init_entry(entry):
                    # If it didn't work, increment number of failed
                    #  entries.
                    failed += 1
                    # Error message.
                    io_utils.print_status(
                      "error", f"Failed to create entry #{x}.", go=True,
                      line_length=self.line_length)
                # end if
            # end for
            # Return number of failed entries.
            return failed
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_init_entries", err)
        # end try
    # end method

    def _init_entry(self, dict_entry):
        """
            Initializes a log entry.

            Arguments:
            - dict_entry -- the dictionary to use to initialize the
               entry.

            Returns:  True if the entry was successfully initialized,
             else False.
           -------------------------------------------------------------
        """
        try:
            # Create a new entry object.
            new_entry = logentry.LogEntry()
            # Try to initialize the entry with info from the
            #  dictionary.
            if new_entry.from_dict(dict_entry):
                # If it worked, add the entry to the log object and
                #  sort lists.
                self.entries.append(new_entry)
                self.sorts[TITLE_SORT].append(
                  (new_entry.title, new_entry.datetime, new_entry.id))
                self.sorts[DATE_SORT].append(
                  (new_entry.datetime, new_entry.title, new_entry.id))
                return True
            else:
                return False
            # end if
        except Exception as err:
            _z_exc("worklog.py/WorkLog/_init_entry", err)
        # end try
    # end method

    def _init_worklog(self, dict_entry):
        """
            Initializes the work log object from data from a file.

            The first log entry read from a data file does not contain
             information about a task; rather, its info attribute holds
             data on the work log itself.

            Arguments:
            - dict_entry -- the list representation of the first log
               entry as read from a data file.

            Returns:  True if data was successfully transferred to the
             work log object; else False.
           -------------------------------------------------------------
        """
        try:
            # Create a dummy log entry object to hold the data.
            new_entry = logentry.LogEntry()
            # Convert the log object information (stored in the info
            #  field of the first entry obuject) into a dictionary.
            new_entry.from_dict(dict_entry)
            # Set the log object's attributes from the dictionary.
            self.total_entries = new_entry.info["total_entries"]
            self.show_help = new_entry.info["show_help"]
            self.last_modified = new_entry.info["last_modified"]
            # But only set the format attributes if the user has not
            #  already set them.
            if not self.date_format:
                self.date_format = new_entry.info["date_format"]
            # end if
            if not self.time_format:
                self.time_format = new_entry.info["time_format"]
            # end if
            return True
        except Exception as err:
            io_utils.print_status(
              "Error", f"Error reading log info:  {err}",
              line_length=self.line_length)
            return False
        # end try
    # end method

# end class
