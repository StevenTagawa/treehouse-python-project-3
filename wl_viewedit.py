"""---------------------------------------------------------------------
    Contains functions to display and edit or delete work log entries.

    Public Functions:
    - browse_entries -- displays a single entry, allowing the user to
       edit, delete, move forward or backwards, or exit.
    - browse_list -- displays a list (or part of a list) of entries,
       allowing the user to select one to view.
    - display_entry -- displays an task which is being edited, including
       both original and changed values.

    Private Functions:
    - _copy_entry -- creates a duplicate of an entry [*unused in this
       implementation].
    - _delete_entry -- deletes an entry; if part of a recurring series,
       allows the user to delete the entire series.
    - _delete_from_series -- deletes a single entry from a recurring
       series.
    - _delete from sort -- deletes an entry from the work log object's
       sorted lists.
    - _edit_entry -- allows the user to edit certain values for an
       entry; if the entry is part of a recurring series, allows the
       user to apply changes to the entire series.
    - _update_entry -- makes changes to an entry as directed by the
       user; if the entry is part of a recurring series and the user so
       wishes, makes changes to all entries in the series.
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

    import io_utils
    import logentry
    import wl_add
    import wl_resource
    import wl_search
except Exception as err:
    _z_exc("wl_viewedit.py/module imports", err)
# end try


# Constants.
QUIT = 0
TITLE = 1
DATE = 2
TIME = 3
DURATION = 4
NOTES = 5
TITLE_SORT = 0
DATE_SORT = 1
ENTRY_ID = 2
DELETE_ONE = 1
DELETE_ALL = 2
DELETE_PARENT = 3
UPDATE_ONE = 1
UPDATE_ALL = 2
TITLE_SORT = 0
DATE_SORT = 1
SORT_KEY = 0
ENTRY_ID = 2


def browse_entries(wl_obj, entry_list, ndx=0):
    """
        Allows the user to browse entries.

        Arguments:
        - wl_obj -- the work log object.
        - entry_list -- the list of entries to browse.

        Keyword Arguments:
        - ndx -- the index of the entry to initially display.

        Returns:  the entry list as modified.
       -----------------------------------------------------------------
    """
    try:
        # Loop.
        while True:
            # If the list is empty, automatically return.
            if len(entry_list) == 0:
                return entry_list
            # end if
            # Clear the screen.
            wl_resource.print_header(wl_obj)
            # Print status message.
            msg = f"Displaying task {(ndx + 1)} of {len(entry_list)}"
            io_utils.print_status(
              "Status", msg, go=True, line_length=wl_obj.line_length)
            # Display the current entry.
            display_entry(wl_obj, entry_list[ndx])
            # Beneath the entry, display a menu.
            options = ["Edit", "Delete"]
            key_list = ["E", "D"]
            if ndx > 0:
                options.append("Previous")
                key_list.append("P")
            # end if
            if ndx < (len(entry_list) - 1):
                options.append("Next")
                key_list.append("N")
            # end if
            options.append("Back")
            key_list.append("B")
            response = io_utils.menu(
              options, keystroke=True, keystroke_list=key_list, lines=False,
              quit_=False, prompt=" ", line_length=wl_obj.line_length)
            # Convert the integer response back into the correct option.
            response = key_list[response - 1]
            # Take the appropriate action.
            if response == "B":
                # If the user wants to go back, return the entry list
                #  (as it may have been modified).
                return entry_list
            elif response == "P":
                # If the user wants to back up one entry, decrement the
                #  index and loop.
                ndx -= 1
                continue
            elif response == "N":
                # If the user wants to go to the next entry, increment
                #  the index and loop.
                ndx += 1
                continue
            elif response == "E":
                # If the user wants to edit the current entry, call the
                #  edit function and then loop.
                _edit_entry(wl_obj, entry_list[ndx], ndx, len(entry_list))
                continue
            else:
                # If the user wants to delete the entry, confirm, and if
                #  confirmed, call the delete function. and then loop.
                if io_utils.confirm("delete this entry"):
                    _delete_entry(wl_obj, entry_list, ndx)
                    # Delete the entry from the entry list.
                    # If there are no more entries, return the empty
                    #  list.
                    if len(entry_list) == 0:
                        return entry_list
                    # end if
                    # If the index is past the end of the list, reset
                    #  it.
                    if ndx <= len(entry_list):
                        ndx = len(entry_list) - 1
                    # end if
                # end if
                continue
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_viewedit.py/browse_entries", err)
    # end try
# end function


def browse_list(wl_obj, browse_list, start=0):
    """
        Presents a list to the user and asks him/her to select one.

        Arguments:
        - wl_obj -- the work log object.
        - browse_list -- the list to present.
        - start -- the first item to display (default 0).

        Returns:  an integer representing an item to display, 0 if the
         user quits, or a string representing a navigational command.
       -----------------------------------------------------------------
    """
    try:
        # If the list is empty, automatically return as if the user had
        #  quit.
        if len(browse_list) == 0:
            return 0
        # end if
        # Clear the screen and print the matches to be listed.
        wl_resource.print_header(wl_obj)
        if len(browse_list) == 1:
            msg = "Showing match 1 of 1"
        else:
            msg = f"Showing matches {start + 1}-"
            if start + 9 <= len(browse_list):
                msg += f"{start + 9} of {len(browse_list)}"
            else:
                msg += f"{len(browse_list)} of {len(browse_list)}"
            # end if
        # end if
        io_utils.print_status(
          "Status", msg, go=True, line_length=wl_obj.line_length)
        # Build the options list.
        options = []
        # For dates, just append the date (as a string).
        if type(browse_list[0]) == datetime.date:
            for ndx in range(start, start + 9):
                # Stop if at the end of the list.
                if ndx == len(browse_list):
                    break
                # end if
                options.append(str(browse_list[ndx]))
            # end for
        # For entries, append the title, date and time (as strings).
        else:
            for ndx in range(start, start + 9):
                # Stop if at the end of the list.
                if ndx == len(browse_list):
                    break
                # end if
                # Gather the fields.
                title = browse_list[ndx].title
                date = wl_resource.format_string(
                  wl_obj, browse_list[ndx].date, short=True)
                time = wl_resource.format_string(wl_obj, browse_list[ndx].time)
                # If the time had a leading zero stripped, replace it
                #  with a space.
                if time[1] == ":":
                    time = f" {time}"
                # end if
                max_title_len = wl_obj.line_length - 23
                # If the title is too long to fit in the column,
                #  truncate it.
                if len(title) > max_title_len:
                    title = title[:max_title_len - 1] + "… "
                else:
                    title += " "
                # end if
                rj = wl_obj.line_length - len(title) - 4
                option = title + f" {date} {time}".rjust(rj, ".")
                # Append the assembled string.
                options.append(option)
            # end for
        # end if
        if start > 0:
            prev = True
        else:
            prev = False
        # end if
        if start + 9 < len(browse_list):
            nxt = True
        else:
            nxt = False
        # end if
        # Now display the menu and return the user's choice.
        return io_utils.menu(
          options, prompt="Select an entry to view:", keystroke_list="#",
          nav=True, prev=prev, nxt=nxt, line_length=wl_obj.line_length)
    except Exception as err:
        _z_exc("wl_viewedit.py/browse_list", err)
    # end try
# end function


def display_entry(wl_obj, entry, edit=False):
    """
        Displays a single log entry.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the entry to display.

        Keyword Arguments:
        - edit -- the entry is being edited.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        print("Title: ", end="")
        if edit and entry.info["title"] != entry.title:
            print(f"{entry.info['title']} -> ", end="")
        # end if
        print(entry.title)
        print("Date: ", end="")
        if edit and entry.info["date"] != entry.date:
            print(
              f"{wl_resource.format_string(wl_obj, entry.info['date'])} -> ",
              end="")
        # end if
        print(wl_resource.format_string(wl_obj, entry.date))
        print("Time: ", end="")
        if edit and entry.info["time"] != entry.time:
            print(
              f"{wl_resource.format_string(wl_obj, entry.info['time'])} -> ",
              end="")
        # end if
        print(wl_resource.format_string(wl_obj, entry.time))
        print("Duration: ", end="")
        if edit and entry.info["duration"] != entry.duration:
            print(
              f"{wl_resource.format_string(wl_obj, entry.info['duration'])}" +
              " -> ", end="")
        # end if
        print(wl_resource.format_string(wl_obj, entry.duration))
        print("Notes: ", end="")
        if edit and entry.info["notes"] != entry.notes:
            print(f"{entry.info['notes']} -> ", end="")
        # end if
        print(entry.notes)
        if entry.recurring:
            print("Recurring:  Yes")
            string = (
              wl_resource.format_recurrance_pattern(
               wl_obj, entry, part=True) + " from " +
              wl_resource.format_string(wl_obj, entry.date, short=True) +
              " until " +
              wl_resource.format_string(
                wl_obj, entry.rec_interval["end"], short=True) + ".")
            io_utils.print_block(string, lf=True)
        elif entry.rec_child_seq:
            print("Recurring:  One of a series")
            parent = wl_search.lookup_entry_by_id(wl_obj, entry.rec_parent)
            print(
              f"Recurrance {entry.rec_child_seq[0]} of " +
              f"{entry.rec_child_seq[1]}.")
            string = (
              wl_resource.format_recurrance_pattern(
               wl_obj, parent, part=True) + " from " +
              wl_resource.format_string(wl_obj, parent.date, short=True) +
              " until " +
              wl_resource.format_string(
                wl_obj, parent.rec_interval["end"], short=True) + ".")
            io_utils.print_block(string, lf=True)
        # end if
        else:
            print("Recurring:  No")
        # end if
        return
    except Exception as err:
        _z_exc("wl_viewedit.py/display_entry", err)
    # end try
# end function


def _copy_entry(entry):
    """
        Creates a duplicate of a log entry object.

        Does not duplicate the info dictionary, which should ordinarily
         be empty).

        Arguments:
        - entry -- the entry to copy.

        Returns:  a copy of the log entry object.
       -----------------------------------------------------------------
    """
    try:
        # Instantiate a new log entry object.
        copy = logentry.LogEntry()
        # Copy each individual attribute.
        copy.id = entry.id
        copy.title = entry.title
        copy.date = entry.date
        copy.time = entry.time
        copy.datetime = entry.datetime
        copy.duration = entry.duration
        copy.notes = entry.notes
        copy.recurring = entry.recurring
        copy.rec_interval = entry.rec_interval
        copy.rec_total = entry.rec_total
        copy.rec_child_seq = entry.rec_child_seq
        copy.rec_parent = entry.rec_parent
        return copy
    except Exception as err:
        _z_exc("wl_viewedit.py/_copy_entry", err)
    # end try
# end function


def _delete_entry(wl_obj, entry_list, ndx):
    """
        Deletes an entry, or a series of entries.

        Determines whether an entry marked for deletion is part of a
         recurring series.  If it is, asks the user whether to delete
         the entire series.

        Arguments:
        - wl_obj -- the work log object.
        - del_entry -- the entry to delete.

        Returns:  the modified entry list.
       -----------------------------------------------------------------
    """
    try:
        # First determine the correct action to take.
        action = None
        # If the entry is part of a series, ask whether to delete just
        #  it, or the entire series.
        if entry_list[ndx].rec_child_seq:
            action = io_utils.menu(
              ["Delete this task only.",
               f"Delete all {entry_list[ndx].rec_child_seq[1]} occurances of" +
               "this task."], keystroke_list="#",
              prompt="This task is part of a recurring series.",
              line_length=wl_obj.line_length)
            # If the user cancels, just return.
            if action == 0:
                return entry_list
            # end if
        # If the entry is the parent of a series, ask the same question.
        elif entry_list[ndx].recurring:
            response = io_utils.menu(
              ["Delete this task only.",
               f"Delete all {entry_list[ndx].rec_total + 1} occurances of " +
               "this task."], keystroke_list="#",
              prompt="This task is the beginning of a recurring series.",
              line_length=wl_obj.line_length)
            # If the user cancels, just return.
            if response == 0:
                return entry_list
            # end if
            # Otherwise set the action.
            if response == 1:
                action = DELETE_PARENT
            else:
                action = DELETE_ALL
            # end if
        # If the entry is not part of any series, just delete it.
        else:
            wl_obj.entries.remove(entry_list[ndx])
            # Delete from the sort lists.
            _delete_from_sort(wl_obj, entry_list[ndx])
            # Delete the entry from the entry list.
            del entry_list[ndx]
        # end if
        # Otherwise take the indicated action.
        if action == DELETE_ONE:
            # Delete from the series.
            _delete_from_series(wl_obj, entry_list[ndx])
            # Delete from the sort lists.
            _delete_from_sort(wl_obj, entry_list[ndx])
            # Delete the entry from the entry list.
            del entry_list[ndx]
        elif action == DELETE_ALL:
            # Set ID to match.
            del_id = entry_list[ndx].rec_parent
            # To delete the entire series, loop through all entries and
            #  delete those in the series, including the original.
            for n in range(len(wl_obj.entries) - 1, -1, -1):
                if (
                  (wl_obj.entries[n].rec_parent == del_id) or
                  (wl_obj.entries[n].id == del_id)):
                    # If the entry is also in the entry list, delete it
                    #  from the list.
                    if wl_obj.entries[n] in entry_list:
                        entry_list.remove(wl_obj.entries[n])
                    # end if
                    # Delete the entry from the sort indexes.
                    _delete_from_sort(wl_obj, wl_obj.entries[n])
                    # Delete the entry from the log.
                    del wl_obj.entries[n]
                # end if
            # end for
        elif action == DELETE_PARENT:
            # When only the parent of a recurring series is deleted, the
            #  first child entry becomes the new parent, and the
            #  attributes of all the other child entries are changed to
            #  reflect that.
            if entry_list[ndx].rec_total > 1:
                # Go through the entries, looking for child entries.
                for n in range(len(wl_obj.entries)):
                    if wl_obj.entries[n].rec_parent == entry_list[ndx].id:
                        # First child entry changes.
                        if wl_obj.entries[n].rec_child_seq[0] == 1:
                            wl_obj.entries[n].recurring = True
                            wl_obj.entries[n].rec_interval = (
                              entry_list[ndx].rec_interval)
                            wl_obj.entries[n].rec_total = (
                              entry_list[ndx].rec_total - 1)
                            wl_obj.entries[n].rec_child_seq = None
                            wl_obj.entries[n].rec_parent = None
                            # Set the new parent ID.
                            new_id = wl_obj.entries[n].id
                        # Changes for all other child entries.
                        else:
                            wl_obj.entries[n].rec_child_seq = (
                              wl_obj.entries[n].rec_child_seq[0] - 1,
                              wl_obj.entries[n].rec_child_seq[1] - 1)
                            wl_obj.entries[n].rec_parent = new_id
                        # end if
                    # end if
                # end for
            # BUT if the first child entry is the ONLY entry in the
            #  series remaining, then it becomes a non-recurring task.
            else:
                # Go through the entries, looking for the one child
                #  entry.
                for n in range(len(wl_obj.entries)):
                    if wl_obj.entries[n].rec_parent == entry_list[ndx].id:
                        # Change the child entry to a regular
                        #  non-recurring task.
                        wl_obj.entries[n].rec_child_seq = None
                        wl_obj.entries[n].rec_parent = None
                        # No need to keep looking.
                        break
                    # end if
                # end for
            # Finally, delete the parent entry.
            wl_obj.entries.remove(entry_list[ndx])
            # Delete from the sort lists.
            _delete_from_sort(wl_obj, entry_list[ndx])
            # Delete the entry from the entry list.
            del entry_list[ndx]
        # end if
        # Set the flag that the work log has changed.
        wl_obj.changed = True
        # Return the modified entry list.
        return entry_list
    except Exception as err:
        _z_exc("wl_viewedit.py/_delete_entry", err)
    # end try
# end function


def _delete_from_series(wl_obj, del_entry):
    """
        Deletes one occurrance from a series of recurring tasks.

        Arguments:
        - wl_obj -- the work log object.
        - del_entry -- the entry to be deleted.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # When deleting a single occurrance from a series, the other
        #  entries in the series must be "cleaned up" to correctly
        #  represent their positions.
        #
        # Get the occurance number and the total number of recurrances.
        occ_num, total_occ = del_entry.rec_child_seq
        # Find the parent entry, reduce the number of recurrances by 1.
        wl_search.lookup_entry_by_id(
          wl_obj, del_entry.rec_parent).rec_total = (total_occ - 1)
        # Now go through the entries, finding and editing the recurrance
        #  data for each child entry.  (Cannot use a for-loop directly
        #  since we are editing the entries.)
        for ndx in range(len(wl_obj.entries)):
            if wl_obj.entries[ndx].rec_parent == del_entry.rec_parent:
                # Only change the recurrance number for recurrances
                #  after the one being deleted.
                if wl_obj.entries[ndx].rec_child_seq[0] > occ_num:
                    wl_obj.entries[ndx].rec_child_seq = (
                      wl_obj.entries[ndx].rec_child_seq[0] - 1, total_occ - 1)
                else:
                    wl_obj.entries[ndx].rec_child_seq = (
                      wl_obj.entries[ndx].rec_child_seq[0], total_occ - 1)
                # end if
            # end if
        # end for
        # Finally delete the child entry.
        wl_obj.entries.remove(del_entry)
        # Set changed flag.
        wl_obj.changed = True
        return
    except Exception as err:
        _z_exc("wl_viewedit.py/_delete_from_series", err)
    # end try
# end function


def _delete_from_sort(wl_obj, del_entry):
    """
        Deletes an entry from the sort indexes.

        Arguments:
        - wl_obj -- the work log object.
        - del_entry -- the entry to delete.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Find the entry in the indexes and delete it.
        for n, entry in enumerate(wl_obj.sorts[TITLE_SORT]):
            if entry[ENTRY_ID] == del_entry.id:
                del wl_obj.sorts[TITLE_SORT][n]
                break
            # end if
        # end for
        for n, entry in enumerate(wl_obj.sorts[DATE_SORT]):
            if entry[ENTRY_ID] == del_entry.id:
                del wl_obj.sorts[DATE_SORT][n]
                break
            # end if
        # end for
        return
    except Exception as err:
        _z_exc("wl_viewedit.py/_delete_from_sort", err)
    # end try
# end function


def _edit_entry(wl_obj, edit_entry, ndx, total):
    """
        Allows the user to edit a log entry.

        Arguments:
        - wl_obj -- the work log object.
        - edit_entry -- the entry to edit.
        - ndx -- the number of the entry being edited.
        - total -- the total number of entries being displayed.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # This function mainly piggybacks on the add functions to alter
        #  the attributes of the log entry object.  All values are
        #  preserved via the info attribute of a working copy until
        #  saved by the user.
        changed = False
        # Create a working copy of the entry to be edited.
        new_entry = _copy_entry(edit_entry)
        # Store the original values in the info attribute.
        new_entry.info["title"] = new_entry.title
        new_entry.info["date"] = new_entry.date
        new_entry.info["time"] = new_entry.time
        new_entry.info["duration"] = new_entry.duration
        new_entry.info["notes"] = new_entry.notes
        new_entry.info["ndx"] = f"task {ndx + 1} of {total}"
        resort = False
        # Loop.
        while True:
            # Clear the screen and display program header.
            wl_resource.print_header(wl_obj)
            # Print status message.
            io_utils.print_status(
              "Status", f"Editing {new_entry.info['ndx']}…", go=True,
              line_length=wl_obj.line_length)
            # Display the entry.
            display_entry(wl_obj, new_entry, edit=True)
            # Print instructions.
            wl_obj.help.print_help(
              wl_obj.show_help, "Editing", "_eh_edit",
              line_length=wl_obj.line_length)
            options = ["Title", "Date", "Time", "Duration", "Notes"]
            # User selects the field to edit.
            response = io_utils.menu(
              options, keystroke_list="#",
              prompt="Please select a field to edit.  When you are finished," +
              " go back to save or discard your changes:",
              line_length=wl_obj.line_length, help_toggle=True)
            # If the user chose to toggle help, do that and loop back.
            if str(response).lower() == "-h":
                wl_obj.show_help = not wl_obj.show_help
                continue
            # end if
            # If the user chose to quit...
            if response == QUIT:
                # If the entry has been edited, prompt to save changes.
                if (
                  changed and
                  io_utils.yes_no("Do you want to save your changes?",
                   line_length=wl_obj.line_length)):
                    # Recalculate the datetime attribute, in case either
                    #  the date or time changed.
                    new_entry.datetime = wl_add.add_datetime(new_entry)
                    # Save the changed values to the original log entry
                    #  object.
                    _update_entry(wl_obj, new_entry, resort)
                    # Set the flag that the log object has changed.
                    wl_obj.changed = True
                # end if
                return
            # Edit title.
            elif response == TITLE:
                ch = wl_add.add_title(wl_obj, new_entry, edit=True)
                # If the title was edited, turn on the resort flag.
                if ch:
                    resort = True
                # end if
            # Edit date.
            elif response == DATE:
                ch = wl_add.add_date(wl_obj, new_entry, edit=True)
                # If the date was edited, turn on the resort flag.
                if ch:
                    resort = True
                # end if
            # Edit time.
            elif response == TIME:
                ch = wl_add.add_time(wl_obj, new_entry, edit=True)
                # If the time was edited, turn on the resort flag.
                if ch:
                    resort = True
                # end if
            # Edit duration.
            elif response == DURATION:
                ch = wl_add.add_duration(wl_obj, new_entry, edit=True)
            # Edit notes.
            else:
                ch = wl_add.add_note(wl_obj, new_entry, edit=True)
            # end if
            # If something was edited, turn on the changed flag.
            if ch:
                changed = True
            # end if
        # end while
    except Exception as err:
        _z_exc("wl_viewedit.py/_edit_entry", err)
    # end try
# end function


def _update_entry(wl_obj, entry, resort):
    """
        Updates a log entry object's attributes with new values.

        Arguments:
        - wl_obj -- the work log object.
        - entry -- the log entry object containing the values to save.
        - resort -- flag that the sort lists will need updating.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # If the edited entry is part of a series (either as the parent
        #  or a child), ask whether to apply the edits to the entire
        #  series or only the one entry--but ONLY if the date attribute
        #  hasn't been changed.  If the date attribute HAS been changed,
        #  apply all the edits to just the one entry, even if other
        #  attributes have also been changed.
        if (
          (entry.recurring is True or entry.rec_parent) and
          (entry.date == entry.info["date"])):
            response = io_utils.menu(
              ["Edit this task only", "Edit all tasks in the series"],
              keystroke_list="#", prompt="This task is part of a series.  " +
              "Do you want to apply your changes to all the tasks in this " +
              "series?", line_length=wl_obj.line_length)
            # If the user chooses to back out, just return without
            #  updating.
            if response == QUIT:
                return
            elif response == UPDATE_ONE:
                edit_series = False
            else:  # response == UPDATE_ALL
                edit_series = True
            # end if
        else:
            edit_series = False
        # end if
        # Find the original entry (and, if applicable, any child
        #  entries).
        for ndx in range(len(wl_obj.entries)):
            if (
              (wl_obj.entries[ndx].id == entry.id) or
              (edit_series and
               ((wl_obj.entries[ndx].rec_parent == entry.rec_parent) or
               (wl_obj.entries[ndx].id == entry.rec_parent)))):
                # Simpler to overwrite the values (even if unchanged).
                wl_obj.entries[ndx].title = entry.title
                wl_obj.entries[ndx].time = entry.time
                wl_obj.entries[ndx].duration = entry.duration
                wl_obj.entries[ndx].notes = entry.notes
                # Recalculate the datetime attribute, in case it's
                #  changed.
                wl_obj.entries[ndx].datetime = (
                  wl_add.add_datetime(wl_obj.entries[ndx]))
                # If title, date or time changed, need to update sort
                #  lists.
                if resort:
                    for n in range(len(wl_obj.sorts[TITLE_SORT])):
                        # Update and re-sort the list.
                        if wl_obj.sorts[TITLE_SORT][n][ENTRY_ID] == entry.id:
                            wl_obj.sorts[TITLE_SORT][n] == (
                              entry.title, entry.datetime, entry.id)
                            wl_obj.sorts[TITLE_SORT].sort()
                        # end if
                    # end for
                    for n in range(len(wl_obj.sorts[DATE_SORT])):
                        # Update and re-sort the list.
                        if wl_obj.sorts[DATE_SORT][n][ENTRY_ID] == entry.id:
                            wl_obj.sorts[DATE_SORT][n] == (
                              entry.datetime, entry.title, entry.id)
                            wl_obj.sorts[DATE_SORT].sort()
                            break
                        # end if
                    # end for
                # end if
            # end if
        # end for
        return
    except Exception as err:
        _z_exc("wl_viewedit.py/_update_entry", err)
    # end try
# end function
