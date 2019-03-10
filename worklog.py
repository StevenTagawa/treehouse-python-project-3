# Imports.
import datetime
import io_utils
import logentry
import wl_add
import wl_help
import wl_resource
import wl_search


# Constants.
TITLE_SORT = 0
DATE_SORT = 1


class WorkLog:
    """-----------------------------------------------------------------
        A work log object.
       -----------------------------------------------------------------
    """
    def __init__(self):
        """-------------------------------------------------------------
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
        """-------------------------------------------------------------
            Override the equality operator to allow work log objects to
             be compared.
           -------------------------------------------------------------
        """
        return self.__dict__ == other.__dict__
    # end method

    def action_get(self):
        """-------------------------------------------------------------
            If the log object is unitialized, ask the user to open or
             create a file.  If the log object is initialized, get an
             action from the user.

            Arguments:  none.

            Returns:  False if the user chooses to exit the program,
             else True.
           -------------------------------------------------------------
        """
        print()
        # If the total_entries attribute is -1, the object is not
        #  initialized.  Ask the user to open or create a log file.
        if self.total_entries == -1:
            keystroke_list = ["O", "N"]
            action = io_utils.menu(
              ["Open log file", "New log file"],
              keystroke=True, keystroke_list=keystroke_list, lines=True,
              top_level=True)
            # If the user chooses to quit here...
            if action == 0:
                # Set the action attribute so _action_take knows to do
                #  nothing.
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
        # If the object has been initialized, skip the above code, print
        #  the header and ask the user what they want to do.
        wl_resource.print_header(self)
        keystroke_list = ["A", "F", "S", "C"]
        action = io_utils.menu(
          ["Add entries", "Find/edit/delete entries", "Save log file",
          "Close log file"], option_type="actions", lines=True,
          keystroke=True, keystroke_list=keystroke_list, top_level=True)
        # If the user chose to quit...
        if action == 0:
            # Set the action attribute to None, which will be a flag for
            #  the action_take method.
            self.action = None
            # If the log object has changed, prompt to save.
            if self.changed == True:
                save = io_utils.yes_no(
                  "The log file has changed.  Do you want to save it?")
                # If yes, just save the file now (bypass action_take so
                #  that it will still exit).
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
    # end method

    def action_take(self):
        """-------------------------------------------------------------
            Takes the action specified in the object's action attribute.
             If the action attribute is set to None, the method
             immediately exits to the main menu.

            Arguments:  none.

            Returns:  True if the user wants to take another action;
             else False, which will break the loop and send the script
             back to the start.  Also False if the user quits.
            ------------------------------------------------------------
        """
        # Flag to the main function on whether or not to loop back to
        #  the beginning.
        # If the action attribute is None, user has quit.  Do nothing.
        #  Return False to ensure that both the inner and outer loop
        #  stop.
        if self.action == None:
            return False
        # Take the action specified:
        # If the user chooses to open a file (at initalization)...
        elif self.action == "O":
            # Try to open and read in a file.  Return whether it
            #  succeeded or failed.  If it succeeded, go to the actions
            #  menu.  If it failed, go to the main menu.
            return self._do_open()
        # If the user chooses to create a file (at initialization)...
        elif self.action == "N":
            # Try to create a file.  Return whether it succeeded or
            #  failed.  If it succeeded, go to the actions menu.  If it
            #  failed, go to the main menu.
            return self._do_create()
        # If the user wants to add entries...
        elif self.action == "A":
            self._do_add()
        # If the user wants look up, copy, edit or delete entries...
        elif self.action == "F":
            self._do_lookup()
        # If the user wants to save the log file (but keep working)...
        elif self.action == "S":
            self._do_save()
        # If the user wants to close the file...
        elif self.action == "C":
            # Close the file and return to the main menu.
            return self._do_close()
        # end if
        # To go back to the actions menu, return True.
        return True
    # end method

    def _do_add(self):
        """-------------------------------------------------------------
            Internal method that adds one or more entry objects to the
             log object.

            Arguments:  none.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        # List of object attributes to set (easier than directly
        #  iterating through the attributes).
        attr_list = [
          "title", "date", "time", "duration", "notes", "recurring"]
        # Initialize list.
        recurring_entries = []
        # Like all of the _do methods, the entire method is inside a
        #  loop, allowing the user to add as many entries as they want.
        not_done = True
        while not_done:
            # First, create a new log entry object.
            new_entry = logentry.LogEntry()
            # Go through the list and set values for each attribute.
            #  Because the user can choose to back up, we don't use a
            #  for loop to iterate through the attributes.
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
                    # If the user goes back a step, clear the previous
                    #  attribute.
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
                # "duration" must be convertible to a timedelta object.
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
                # "recurring" will either be True of False, and if True
                #  will also return a list of recurrance date objects.
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
                    wl_resource.print_status(
                      "status",
                      msg="Addition of this task has been cancelled.")
                    # If the user aborts and does not want to start
                    #  another task, return immediately.
                    if not io_utils.yes_no("Do you want to add another task?"):
                        return
                else:
                    attrib += go
                # end if
            # end while
            # Set the datetime attribute.
            new_entry.datetime = wl_add.add_datetime(new_entry)
            # Add the entry to the work log.
            self._do_sort(new_entry)
            self.entries.append(new_entry)
            # Now add the recurring entries, if any.
            self._do_add_recurring_entries(new_entry, recurring_entries)
            # And update.
            self.total_entries = len(self.entries)
            # Note the log object has changed, and the time.
            self.changed = True
            self.last_modified = datetime.datetime.now()
            # Build status message.
            if recurring_entries:
                msg = f"{len(recurring_entries) + 1} entries added."
            else:
                msg = "Entry added."
            # Print that the entry was added.
            wl_resource.print_status("status", msg=msg)
            # Finally, ask the user if they want to add another entry.
            #  (Whether they are done will be the opposite of their
            #  answer.)
            not_done = (io_utils.yes_no("Do you want to add another task?"))
        # end while
        return
    # end method

    def _do_add_recurring_entries(self, entry, recurrance_list):
        """-------------------------------------------------------------
            Creates recurring entries based on a template entry and adds
             them to the work log object.

            Arguments:
            - entry -- the original entry.
            - recurrance_list -- the list of recurring dates.

            Returns:  nothing.
           -------------------------------------------------------------
        """
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
    # end method

    def _do_close(self):
        """-------------------------------------------------------------
            Internal method that closes the work log object, leaving it
             to be overwritten by a new instance (if the user chooses to
             work with a new file) or destroyed upon program exit.
             Calls _do_save.

            Arguments:  none.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        if self.changed and io_utils.yes_no(
          f"{self.filename} has changed.  Do you want to save it?"):
            if not self._do_save(self):
                wl_resource.print_status("error", msg="Error saving file.")
            # end if
        else:
            wl_resource.print_status("status", msg=f"{self.filename} closed.")
        return False
    # end method

    def _do_create(self):
        """-------------------------------------------------------------
            Creates a new file to store data from the log object.  May
             call _do_open.

            Arguments:  none.

            Returns:  True if successful; False if there was an error or
             the user aborts the process.
           -------------------------------------------------------------
        """
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
            wl_resource.print_status("status", f"{self.filename} created.")
            return True
        # end if
    # end method

    def _do_lookup(self):
        """-------------------------------------------------------------
            Searches for and displays one or more log entries.

            Arguments:  none.

            Returns:  True if successful; False if the user aborted.
           -------------------------------------------------------------
        """
        # Clear the screen.
        wl_resource.print_header(self)
        # If there are no entries in the log, tell the user and then
        #  return.
        if len(self.entries) == 0:
            wl_resource.print_status(
              "error", msg="There are no tasks in the log to search!")
            return False
        # end if
        # Main menu.
        option_list = [
          "By Date/Time", "By Duration", "By Text Search", "By Pattern"]
        prompt = "Please select a method by which to find entries:"
        search_opt = io_utils.menu(
          option_list, keystroke_list = "#", prompt=prompt)
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
    # end method

    def _do_open(self):
        """-------------------------------------------------------------
            Opens a log file and reads data into the log object.

            Arguments:  none.

            Returns:  True if successful; False if there was an error.
           -------------------------------------------------------------
        """
        # If we don't have a filename, get one.
        if self.filename == "":
            self.filename = io_utils.get_filename_open(filetype="csv")
        # end if
        # If self.filename is still empty, the user chose to go back, so
        #  just return.
        if self.filename == "":
            return False
        # end if
        # Open and read the file.
        entry_dict = io_utils.file_read(self.filename, filetype="csv")
        if not entry_dict:
            return False
        # The first entry contains data on the log object.
        new_entry = logentry.LogEntry()
        try:
            # Convert the log object information (stored in the info field
            #  of the first entry obuject) into a dictionary.
            new_entry.from_dict(entry_dict[0])
            self.total_entries = new_entry.info["total_entries"]
            self.date_format = new_entry.info["date_format"]
            self.time_format = new_entry.info["time_format"]
        except:
            wl_resource.print_status("error", "Error reading log info.")
            return False
        # end try
        # Get rid of the first entry.
        del entry_dict[0]
        # Then iterate through the list of entries.
        for x, entry in enumerate(entry_dict):
            # Create a new entry object.
            new_entry = logentry.LogEntry()
            # Initialize the entry with info from the dictionary.
            new_entry.from_dict(entry)
            # If the ID attribute is not blank, the entry was
            #  successfully initialized.  Make sure the critial fields
            #  were converted to the correct types.
            if (
              type(new_entry.id) == int and type(new_entry.date) ==
              datetime.date and type(new_entry.time) == datetime.time and
              type(new_entry.datetime) == datetime.datetime and
              type(new_entry.duration) == datetime.timedelta):
                # Add the valid entry to the log object and sort lists.
                self.entries.append(new_entry)
                self.sorts[TITLE_SORT].append(
                  (new_entry.title, new_entry.datetime, new_entry.id))
                self.sorts[DATE_SORT].append(
                  (new_entry.datetime, new_entry.title, new_entry.id))
            else:
                # Error message.
                wl_resource.print_status(
                  "error", f"Failed to create entry #{x}.", go=True)
            # end if
        # end for
        # Once all the entries have been added, sort the lists.
        self.sorts[TITLE_SORT].sort()
        self.sorts[DATE_SORT].sort()
        # Print final status.
        wl_resource.print_status(
          "status",
          msg=f"{self.filename} opened.  {self.total_entries} entries read.")
        return True
    # end method

    def _do_save(self):
        """-------------------------------------------------------------
            Saves the log file (but allows the user to continue working
             with the log object).

            Arguments:  none.

            Returns:  True if successful; False if there was an error.
           -------------------------------------------------------------
        """
        # Initialize a temporary list to hold the log data.
        entry_list = []
        # Create a dummy entry object, which will hold data for the log
        #  object.
        new_entry = logentry.LogEntry()
        fn = new_entry.FIELDNAMES
        new_entry.info = {
          "total_entries": self.total_entries, "date_format": self.date_format,
          "time_format": self.time_format, "show_help" : self.show_help,
          "last_modified" : self.last_modified}
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
            wl_resource.print_status("status", f"{self.filename} saved.")
            self.changed = False
            return True
        else:
            return False
        # end if
    # end method

    def _do_sort(self, entry, update=False):
        """-------------------------------------------------------------
            Maintains and updates the sort indexes for the entries in a
             log object.

            Arguments:
            - entry -- an entry to add or update.

            Keyword arguments:
            - update -- the update flag (default False).

            Returns:  nothing.
            ------------------------------------------------------------
        """
        # The log object maintains two sort indexes of its entries:  by
        #  title and by datetime.  Two sorted lists are stored in the
        #  log object's sorts attribute.  Each list consists of a series
        #  of tuples, containing the key to be sorted, the title or
        #  date/time, and the ID of the associated entry.
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
    # end method
