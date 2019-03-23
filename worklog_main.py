"""
    Script for Project 3 of the Treehouse Python Techdegree, Work Log.

    Public Functions:
    - main -- the main script.

    Private Functions:
    - _z_exc -- generic exception handler.
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
    import io_utils
    import worklog
except Exception as err:
    _z_exc("worklog_runme.py/module imports", err)
# end try


def main():
    """
        Main script for the program.

        Arguments:  none.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # The preferences variable is a dictionary that contains any
        #  variables which must persist between instances of the work
        #  log object.
        preferences = {}
        # At the beginning of the program's run, turn help on (the user
        #  can toggle this off and on during the run).
        preferences["show_help"] = True
        # Also at the beginning of the run, set the default line length
        #  (the user can change this during the run.)
        preferences["line_length"] = 80
        # Print welcome screen.
        io_utils.welcome_screen(3, "Work Log!", preferences["line_length"])
        # Outer loop, cycles until the user chooses to exit the program.
        running = True
        while running:
            # Create a new work log object.
            work_log = worklog.WorkLog()
            # Set the object's show_help attribute.
            work_log.show_help = preferences["show_help"]
            # Set the line length.
            work_log.line_length = preferences["line_length"]
            # Inner loop, starts by initializing the log object from a
            #  file, or creating a new file.  If the user exits out of
            #  the open or create file process, or chooses to close the
            #  log file, the inner loop will stop and the outer loop
            #  will cycle again.  Otherwise the inner loop will perform
            #  actions chosen by the user.
            working = True
            while working:
                # Get an action from the user.  If the user chooses to
                #  quit, the log object will set the flag to end the
                #  program.
                running = work_log.action_get()
                # Take the action.  If the user chose to quit during the
                #  action_get method, the work log object's action
                #  attribute will be set so that this method does
                #  nothing.
                working = work_log.action_take()
            # end while
            # Before looping back to the main menu, pass the current
            #  values for show_help and line_length back to the
            #  function.
            preferences["show_help"] = work_log.show_help
            preferences["line_length"] = work_log.line_length
        # end while
        # User chose to quit.
        io_utils.goodbye_screen(
          "Work Log", line_length=preferences["line_length"])
        return
    except Exception as err:
        _z_exc("worklog_runme.py/main", err)
    # end try
# end function


# PROGRAM STARTS HERE
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # If not loaded into another module, run the main script.
    main()
# end if
# end program
