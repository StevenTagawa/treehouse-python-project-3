"""---------------------------------------------------------------------
    This is the script file for Project 3 of the Treehouse Python
    Techdegree, Work Log.
   ---------------------------------------------------------------------
"""

# Imports.
import io_utils
import worklog


def main():
    """-----------------------------------------------------------------
        Main script for the program.

        Arguments:  none.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    # The preferences variable is a dictionary that contains any
    #  variables which must persist between instances of the work log
    #  object.
    preferences = {}
    # At the beginning of the program's run, turn help on (the user can
    #  toggle this off and on during the run).
    preferences["show_help"] = True
    # Print welcome screen.
    io_utils.welcome_screen(3, "Work Log!")
    # Outer loop, cycles until the user chooses to exit the program.
    running = True
    while running:
        # Create a new work log object.
        work_log = worklog.WorkLog()
        # Set the object's show_help attribute.
        work_log.show_help = preferences["show_help"]
        # Inner loop, starts by initializing the log object from a file,
        #  or creating a new file.  If the user exits out of the open or
        #  create file process, or chooses to close the log file, the
        #  inner loop will stop and the outer loop will cycle again.
        #  Otherwise the inner loop will perform actions chosen by the
        #  user.
        working = True
        while working:
            # Get an action from the user.  If the user chooses to quit,
            #  the log object will set the flag to end the program.
            running = work_log.action_get()
            # Take the action.  If the user chose to quit during the
            #  action_get method, the work log object's action attribute
            #  will be set so that this method does nothing.
            working = work_log.action_take()
        # end while
        # Before looping back to the main menu, pass the current state
        #  of the show_help flag back to the function.
        preferences["show_help"] = work_log.show_help
    # end while
    # User chose to quit.
    print()
    print(
      "-=-=-{Goodbye}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("Thanks for using Work Log!")
    print(
      "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    return
# end function


# PROGRAM STARTS HERE
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # If not loaded into another module, run the main script.
    main()
# end if
# end program
