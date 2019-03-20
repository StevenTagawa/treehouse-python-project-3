"""---------------------------------------------------------------------
    Contains i/o-related functions.

    Public Functions:
    - build_dict_string -- converts a dictionary into a string
       equivalent (i.e., the literal representation of the dictionary
       in code).
    - clear_screen -- clears the screen (if supported by the console).
    - del_from_list -- deletes all items from a list that meet
       specified criteria.
    - confirm -- asks the user to confirm a choice.
    - file_create -- creates a file specified by the user.
    - file_read -- opens and reads data from a specified file.
    - file_write -- writes data to a specified file.
    - get_filename_open -- asks the user for the name of a file to open.
    - get_input -- prints a prompt and gets a string, int or float from
       the user.
    - goodbye_screen -- prints a goodbye message
    - menu -- prints a menu and gets a choice from the user.
    - print_block -- prints or returns a string broken at a specified
       column width.
    - print_status -- prints a status message.
    - welcome_screen -- prints an initial screen.
    - yes_no -- gets the user's answer to a yes/no question.

    Private Functions:
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
    import csv
    import os
    import re

    import str_utils
    import wl_resource
except Exception as err:
    _z_exc("io_utils.py/module imports", err)
# end try


def build_dict_string(dic):
    """-----------------------------------------------------------------
        Builds and returns a string representation of a dictionary.

        Arguments:
        - dic -- the dictionary to process.

        Returns:  the string representing the dictionary.
       -----------------------------------------------------------------
    """
    try:
        # Why to build a string representation piecemeal instead of just
        #  using str:  The str method, when used on a whole dictionary
        #  (as opposed to a specific item), returns the __repr__ of each
        #  item, rather than the __str__.  For built-in types these two
        #  values are the same, but for other objects (notably datetime
        #  objects) they may not be.
        #
        # If the function is passed an empty dictionary, just return the
        #  string representation of that.
        if not dic:
            return "{}"
        # end if
        string = "{"
        # Loop through the dictionary, getting strings for each key and
        #  value.
        for key, value in dic.items():
            string += str(key) + ": " + str(value) + ", "
        # end for
        # Strip the last comma and space and close.
        string = string[:-2] + "}"
        return string
    except Exception as err:
        _z_exc("io_utils.py/build_dict_string", err)
    # end try
# end function


def clear_screen():
    """-----------------------------------------------------------------
        Clears the screen.

        Arguments:  None.

        Returns:  Nothing.
       -----------------------------------------------------------------
    """
    try:
        # This print line is a marker for those terminals/shells which
        #  refuse to implement the system call.  For those terminals/shells
        #  that do, this line will instantly disappear.
        print(
          "SCREENCLEARSHERE SCREENCLEARSHERE SCREENCLEARSHERE")
        os.system("cls" if os.name == "nt" else "clear")
        return
    except Exception as err:
        _z_exc("io_utils.py/clear_screen", err)
    # end try
# end function


def del_from_list(lst, condition, index=None, attr=None):
    """-----------------------------------------------------------------
        Deletes all items in a list that meet a condition.

        Arguments:
        - lst -- the list from which to delete items.
        - condition -- the criterion for deletion.

        Keyword Arguments:
        - index -- subitem within the item to search.
        - attr -- object attribute to search.

        Returns:  the number of items deleted.
       -----------------------------------------------------------------
    """
    try:
        d = 0
        # Loop through the list backwards.
        for n in range(len(lst)-1, -1, -1):
            # If the item matches, delete it.
            if index is not None:
                if lst[n][index] in condition:
                    del lst[n]
                    d += 1
                # end if
            elif attr is not None:
                if getattr(lst[n], attr) in condition:
                    del lst[n]
                    d += 1
            elif lst[n] in condition:
                del lst[n]
                d += 1
            # end if
        # end for
        return d
    except Exception as err:
        _z_exc("io_utils.py/del_from_list", err)
    # end try
# end function


def confirm(prompt, line_length=80):
    """-----------------------------------------------------------------
        Asks the user to confirm a decision.

        Arguments:
        - prompt -- descriptive text of what ot confirm.
        - line_length -- the width of the screen in characters (default
           80)

        Returns:  True if the user confirms, otherwise False.
       -----------------------------------------------------------------
    """
    try:
        # Unlike the yes_no function, confirm doesn't loop seeking a
        #  valid answer.  It treats "Y" (or "y") as confirmation, and
        #  any other input as non-confirmation.
        #
        # Print the header line.
        print("\n-=-=-{Confirm}", end="")
        char = "-"
        for n in range(15, line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Get the response.  If it isn't a "y", assume the answer is no.
        response = input(
          print_block(
            "Are you sure you want to " + prompt + "? [Y/N]:  ",
            lf=False, ret_str=True, line_length=line_length))
        if re.match(r"y", response, re.I):
            return True
        else:
            return False
        # end if
    except Exception as err:
        _z_exc("io_utils.py/confirm", err)
    # end try
# end function


def file_create(filetype="txt", line_length=80):
    """-----------------------------------------------------------------
        Creates a new file to store data.  Offers to overwrite an
         existing file.

        Keyword Arguments:
        - filetype -- the type of file to create (default "txt").
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  The name of the file created, or an empty string if
         unsuccessful; and a bool, which is True only if the named file
         exists and the user wants to open it.
       -----------------------------------------------------------------
    """
    try:
        fname = ""
        while not fname:
            fname = get_input(
              prompt="Please enter a name for the new file (press [ENTER] " +
              "to go back).\n")
            if not fname:
                # If the user entered nothing, ask if they want to go
                #  back.
                exit = yes_no(
                  "You did not enter a name.  Do you want to go back?")
                if exit:
                    # User wants to exit.  Return an empty string.
                    return "", False
                else:
                    # Loop back to getting a filename.
                    continue
                # end if
            else:
                # If user did not manually put in an extension, add it.
                if fname[-4:].lower() != ("." + filetype):
                    fname += "." + filetype
                # end if
                # Check to see if the file exists.
                if os.path.isfile(fname):
                    # If the file exists, ask the user if they want to
                    #  use the file, overwrite the file, or create a new
                    #  file with a different name.
                    print_status(
                      "Warning", f"{fname} already exists.", go=True,
                      line_length=line_length)
                    choice = menu(
                            ["Open this file.", "Replace this file",
                             "Create a new file with a different name"],
                            confirm=True, keystroke=True,
                            keystroke_list=["O", "R", "C"], lines=True)
                    # If the user chose to quit, return an empty string.
                    if choice == 0:
                        return "", False
                    elif choice == 1:
                            # The user chose to open this file.  Return
                            #  the filename and flag to open the file.
                        return fname, True
                    elif choice == 2:
                        # The user chose to replace the existing
                        #  file.  Return the filename (as though the
                        #  file were being created).
                        return fname, False
                    else:
                        # User chose to try with a different name.  Set
                        #  fname back to an empty string and skip to the
                        # end of the loop.
                        fname = ""
                        continue
                    # end if
                # end with
                else:
                    # File doesn't exist (good).  Test create the file
                    # just to make sure it will work.
                    try:
                        with open(fname, "w", newline="") as data_file:
                            data_file.write("TEST")
                            return fname, False
                    except Exception as err:
                        print_status(
                          "Error",
                          f"An error occured while creating the file:  {err}",
                          line_length=line_length)
                        # Ask the user if they want to try again or go
                        #  back.
                        if yes_no("Do you want to try again?"):
                            # User wants to exit.
                            return "", False
                        # end if
                        # Loop back to getting a filename.
                        continue
                        # end if
                    # end try
                # end if
            # end if
        # end while
        # Unless something went wrong along the way, return the file
        #  name.
        return fname, False
    except Exception as err:
        _z_exc("io_utils.py/file_create", err)
    # end try
# end function


def file_read(fname, filetype="txt", line_length=80):
    """-----------------------------------------------------------------
        Opens and reads a file.

        Arguments:
        - fname -- the name of the file to open.

        Keyword Arguments:
        - filetype -- the extension of the file to open or create
           (default txt).
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  a data element.  For a txt file, a list containing the
         lines of text in the file; for a csv file, a list of
         dictionaries containing the data in the file.  If the open or
         read operation failed, an empty list.

       -----------------------------------------------------------------
    """
    # Open and read the file.
    try:
        with open(fname, "r", newline="") as data_file:
            if filetype == "txt":
                data_list = list(data_file)
            elif filetype == "csv":
                data_list = list(csv.DictReader(data_file, delimiter=","))
            else:
                # If the file type doesn't match any known type, return
                #  an error.
                print_status(
                  "Error", "Unrecognized file type.", line_length=line_length)
                return []
            # end if
            return data_list
        # end with
    except Exception as err:
        print_status(
          "Error", f"An error occured while reading the file:  {err}",
          line_length=line_length)
        return []
    # end try
# end function


def file_write(fname, filetype, data_list, fieldnames=None, line_length=80):
    """-----------------------------------------------------------------
        Opens a file and writes data to it.

        Arguments:
        - fname -- the name of the file to open.
        - filetype -- the type of file (the function does not check to
            ensure that the file type matches the extension).

        Keyword Arguments:
        - fieldnames -- for csv files, the field names of the dictionary
           to be written.
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  True if the open/write operation succeeded, False
         otherwise.
       -----------------------------------------------------------------
    """
    # Open the file.
    try:
        with open(fname, "w", newline="") as file:
            if filetype == "txt":
                for line in data_list:
                    file.write(line)
                # end for
            else:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            # end if
        # end with
    except OSError as err:
        print_status(
          "Warning", f"Error writing log file:  {err}",
          line_length=line_length)
        return False
    # end try
    return True
# end function


def get_filename_open(filetype, line_length=80):
    """-----------------------------------------------------------------
        Gets the name of a file to open.  On request, displays a list of
         files in the working directory and allows the user to choose
         one.

        Arguments:
        - filetype -- extension of the file to open.
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  the name of the file to open.
       -----------------------------------------------------------------
    """
    try:
        valid = False
        while not valid:
            prompt = (
              "Enter the name of the file you want to open, or [?] to see a " +
              "list of available files.  Enter [Q] to go back.")
            fname = get_input(prompt=prompt)
            # If the user didn't enter anything, print a message and
            #  loop back.
            if not fname:
                print_status(
                  "Error", "You did not enter anything.",
                  line_length=line_length)
                continue
            if fname.lower() == "q":
                # If the user backs out, set the filename to an empty
                #  string and set the loop to end.
                fname = ""
                valid = True
            elif fname != "?":
                # If the user specified a filename but did not type the
                #  extension, add it now.
                if fname[-4:].lower() != ("." + filetype):
                    fname += "." + filetype
                # end if
                # Then check to make sure the file exists.
                if os.path.isfile(fname):
                    # Set the loop to end with the complete filename.
                    valid = True
                else:
                    # Print a warning message and loop back.
                    print_status(
                      "Error", f"File {fname} not found.",
                      line_length=line_length)
                # end if
            else:
                # Scan the directory and present a menu of available
                #  files.
                files = os.listdir()
                if not files:
                    # If there were no files in the directory, go back
                    #  to the previous menu.
                    print_status(
                      "Warning", "No available files found.",
                      line_length=line_length)
                    fname = ""
                    valid = True
                else:
                    # remove any files of the wrong filetype.
                    temp = []
                    for f in files:
                        if f[-3:] == filetype:
                            temp.append(f)
                        # end if
                    # end for
                    files = temp
                    # If no files of the right filetype were found, go
                    #  back to the previous menu.
                    if len(files) == 0:
                        print_status(
                          "Warning", "No available files found.",
                          line_length=line_length)
                        fname = ""
                        valid = True
                    else:
                        # Show a menu of the available files, keyed by
                        #  number.
                        choice = menu(
                            files, option_type="files", keystroke=True,
                            keystroke_list="#", lines=True)
                        if choice:
                            fname = files[choice - 1]
                            valid = True
                        # end if
                    # end if
                # end if
            # end if
        # end while
        return fname
    except Exception as err:
        _z_exc("io_utils.py/get_filename_open", err)
    # end try
# end function


def get_input(prompt, typ="str", must_respond=True, line_length=80):
    """-----------------------------------------------------------------
        Prompts for input from the user.

        Arguments:
        - prompt -- the prompt to display (default ">>").

        Keyword arguments:
        - typ -- the type of input to return (default "str").
        - must_respond -- user must provide a response (default True).
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  a string with the user's input; None if a specific
         type is required and the user's input cannot be converted to
         that type.
       -----------------------------------------------------------------
    """
    try:
        # Loop.
        while True:
            # Print the header line.
            print("\n-=-=-{Input}", end="")
            char = "-"
            for n in range(12, line_length):
                print(char, end="")
                if char == "-":
                    char = "="
                else:
                    char = "-"
                # end if
            # end for
            print()
            # Print the prompt text.
            print_block(prompt, line_length=line_length)
            # Put the prompt itself on the next line, and get a response.
            response = input(">>  ")
            # If the user must respond, check to make sure the response
            #  isn't empty, and if it is, loop back.
            if response or (not must_respond):
                break
            # end if
            print_status(
              "Error", "You did not enter anything.", line_length=line_length)
        # end while
        # If the caller wants a string, just return.
        if typ == "str":
            return response
        # end if
        # If the caller wants a different built-in type, try to convert
        #  the response, and return None if there is an exception.
        try:
            if typ == "int":
                response = int(response)
                return response
            elif typ == "float":
                response = float(response)
                return response
            # end if
        except ValueError:
            return None
        # end try
        # If the type wasn't recognized, just return the raw input.
        return response
        # end if
    except Exception as err:
        _z_exc("io_utils.py/get_input", err)
    # end try
# end function


def goodbye_screen(project_name, line_length=80):
    """-----------------------------------------------------------------
        Prints a thank you message.

        Arguments:
        - project_name -- the name of the project.

        Keyword Arguments:
        - line_length -- the width of the screen in characters (default
           80).

        Returns:  Nothing
       -----------------------------------------------------------------
    """
    try:
        # Print header line.
        begin = "-=-=-{Goodbye}"
        print(begin, end="")
        char = "-"
        for n in range(14, line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Print message.
        print(f"Thanks for using {project_name}!")
        # Print footer line.
        char = "-"
        for n in range(line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        return
    except Exception as err:
        _z_exc("io_utils.py/goodbye_screen", err)
    # end try
# end function


def menu(
  options, option_type="options", confirm=False, keystroke=False,
  keystroke_list=[], match_case=False, multiple=False, lines=True, columns=1,
  col_dir="down", validate_all=False, show_help=False, help_text="",
  top_level=False, prompt="", quit_=True, nav=False, prev=False, nxt=False,
  header="", help_toggle=False, line_length=80):
    """-------------------------------------------------------------
        Presents a menu and obtains a response from the user.

        Arguments:
        - options -- list of options from which to choose.  It is the
           caller's responsibility to ensure that option strings are not
           longer than line_length (or line_length minus the 4 spaces
           needed to display the associated number or keystroke option);
           if they are, they will be truncated.

        Keyword Arguments:
        - option_type -- word or phrase describing the options, used to
           build a generic prompt; ignored if prompt is passed (default
           "options").
        - confirm -- asks the user to confirm his/her choice(s) before
           returning (default False).***
        - keystroke -- specifies selection by shortcut (default False).
        - keystroke_list -- list of shortcuts corresponding to the
           options; ignored if keystroke is False, unless it is "#",
           which specifies selection by number (default empty list).
           (NOTE:  "Q" is reserved for the quit option and cannot be
           included in the list).
        - match_case -- requires the user's response(s) to match the
           case of the option(s) (default False).
        - multiple -- allows the selection of multiple options (default
           False).
        - lines -- print each option on a separate line; ignored if
           columns > 1 (default True).
        - columns -- number of columns in which to arrange the options;
           can be 1 to 3 (default 1).***
        - col_dir -- direction in which to arrange the options in a
           multi-column display; ignored if columns = 1 (default
           "down").***
        - validate_all -- requires all choices made by the user to be
           valid options (defualt False)
        - show_help -- allows the user to choose to see a help screen
           before making his/her choice(s) (default False).***
        - help_text -- the help text to show the user; ignored if
           show_text is False (default empty string).***
        - top_level -- flag indicating a top-level menu (default False).
        - prompt -- the prompt to display (default empty string).
        - quit_ -- allows the user to quit/abort/go back (default True).
        - nav -- prints additional navigational choices; ignored unless
           the menu choices are numbered (default False).
        - prev -- prints the choice to move backards; ignored if nav is
           False (default False).
        - nxt -- prints the choice to move forwards; ignored if nav is
           False (default False).
        - header -- prints a header line before the first option (but
           after the quit option, if quit_ is True) (default empty
           string).  It is the caller's responsibility to ensure that
           the header is not longer than line_length; if it is, it will
           be truncated.
        - help_toggle -- enables menu to return "-h" as a command to
           toggle help (default False).
        - line_length -- the width of the screen in characters (default
           80).
        ***(Not currently implemented.)

        Returns:
         if quit_ is True and the user chooses to quit, 0;
         if multiple is False, an 1-based integer representing the
          user's choice;
         if multiple is True, a list of 1-based integers representing
          the user's choices.
         if nav is True and the user so enters, "-p" or "-n";
         if help_toggle is True and the user so enters, "-h".
       -------------------------------------------------------------
    """
    try:
        # Make sure the column argument is valid.
        if not (0 < columns <= 3):
            columns = 1
        # end if
        # Disable nav unless the menu choices are numbered.
        if keystroke_list != "#":
            nav = False
        # end if
        # Build the menu display.
        display_list = _menu_build_display_list(
          options, option_type, prompt, keystroke, keystroke_list, line_length,
          multiple, quit_, top_level, header)
        # Run this part in a loop until a valid response is entered.
        while True:
            # Display the menu.
            _menu_display(
              display_list, prompt, lines, multiple, nav, prev, nxt,
              line_length)
            # Get a response.  If the user didn't enter anything, loop
            #  back.
            response_list = _menu_get_response(line_length)
            if response_list is None:
                continue
            # end if
            response_list = _menu_evaluate_response(
              response_list, options, keystroke, keystroke_list, multiple,
              validate_all, match_case, quit_, nav, help_toggle, line_length)
            if response_list is not None:
                return response_list
            # end if
        # end while
    except Exception as err:
        _z_exc("io_utils.py/menu", err)
    # end try
# end function


def print_block(string, line_length=80, lf=True, ret_str=False):
    """-----------------------------------------------------------------
        Takes a long string and prints it within a specified width.

        Arguments:
        - string -- the string to print.

        Keyword Arguments:
        - line_length -- the desired line length (default 80).
        - lf -- print a line feed after the block (default True)
        - ret_str -- flag to return a string rather than print it.

        Returns:  if string is True, a formatted string; else nothing.
       -----------------------------------------------------------------
    """
    try:
        if ret_str:
            r_str = ""
        # end if
        # Break the string into words, along spaces, hyphens, and
        #  newlines.
        word_list = re.split(r"(\s)|(-)|(¤)", string)
        col = 0
        for word in word_list:
            # Filter out None.
            if word:
                # If the word is a newline character, always print (or
                #  add) a new line, and reset the column counter.
                if word == "¤":
                    if ret_str:
                        r_str += "\n"
                    else:
                        print()
                    # end if
                    col = 0
                # If there is EXACTLY one character left on the line--
                elif col == line_length - 1:
                    # If the word is a space or a hyphen, print or add
                    #  it, and then a new line, and reset the column
                    #  counter.
                    if word in [" ", "-"]:
                        if ret_str:
                            r_str += word + "\n"
                        else:
                            print(word)
                        # end if
                        col = 0
                    # If the word is anything else, print or add a new
                    #  line, then the word, and reset the column
                    #  counter.
                    else:
                        if ret_str:
                            r_str += "\n" + word
                        else:
                            print("\n" + word, end="")
                        # end if
                        col = len(word)
                    # end if
                # In all other cases--
                else:
                    # Print or add the word if it won't run past the end
                    #  of the line, and increment the column counter.
                    if col + len(word) < line_length:
                        if ret_str:
                            r_str += word
                        else:
                            print(word, end="")
                        # end if
                        col += len(word)
                    # If it would run past the end of the line, print or
                    #  add a new line, then the word, and reset the
                    #  column counter.
                    else:
                        if ret_str:
                            r_str += "\n" + word
                        else:
                            print("\n" + word, end="")
                        # end if
                        col = len(word)
                    # end if
                # end if
            # end if
        # end for
        # Print or add a newline at the end if called for.
        if lf:
            if ret_str:
                r_str += "\n"
            else:
                print()
            # end if
        # end if
        # Return the string if called for; otherwise we're done.
        if ret_str:
            return r_str
        else:
            return
        # end if
    except Exception as err:
        _z_exc("io_utils.py/print_block", err)
    # end try
# end function


def print_status(msg_type, msg, go=False, line_length=80):
    """-----------------------------------------------------------------
        Prints a status or error message, optionally waits for the user
         to press [ENTER] to continue.

        Arguments:
        - msg_type -- the type of status to print.
        - msg -- the message to print

        Keyword Arguments:
        - go -- return without waiting for the user (default False).
        - line_length -- the width of the screen in characters (default
           80)

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Print the beginning of the header line.
        begin = "\n-=-=-{" + msg_type.title() + "}"
        print(begin, end="")
        # Print the remainder of the header line.
        if len(begin) % 2 == 1:
            char = "-"
        else:
            char = "="
        # end if
        for n in range(len(begin) - 1, line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Print the message.
        if len(msg) < line_length:
            print(msg)
        else:
            print_block(msg, line_length=line_length)
        # end if
        # Print the footer line.
        char = "-"
        for n in range(line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Optionally wait for the user.
        if not go:
            input("Press [ENTER] to continue.")
        # end if
        return
    except Exception as err:
        _z_exc("io_utils.py/print_status", err)
    # end try
# end function


def welcome_screen(project_no, project_name, line_length):
    """-----------------------------------------------------------------
        Clears the screen and prints introductory text.

        Arguments:
        - project_no -- the number of the project.
        - project_name -- the name of the project.
        - line_length -- the initial width of the screen in characters.

        Returns:  Nothing
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen.
        clear_screen()
        # Print the header line.
        print("-=-=-{Welcome}", end="")
        char = "-"
        for n in range(14, line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # Print the welcome message.
        print(
          "Treehouse Python Techdegree Project #" +
          str(project_no) + ":")
        print(project_name)
        print("-" * (line_length))
        print("Implemented by Steven Tagawa")
        # Print the footer line.
        char = "-"
        for n in range(line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        return
    except Exception as err:
        _z_exc("io_utils.py/welcome_screen", err)
    # end try
# end function


def yes_no(prompt, clear=False, quit_=False, line_length=80):
    """-----------------------------------------------------------------
        Prompts the user to answer a yes or no question.

        Arguments:
        - prompt -- The question to be answered.

        Keyword arguments:
        - clear -- Clear the screen first (default False).
        - quit_ -- Allow the user to go back or quit (default False).
        - line_length -- the width of the screen in characters (default
           80)

        Returns:  True if the user answers yes, False if no.  If quit_ is
         True, will also return "-b" or "-q" if the user enters it.
       -----------------------------------------------------------------
    """
    try:
        # Clear the screen if applicable.
        if clear:
            clear_screen()
        # Run in a loop until a valid response is obtained.
        while True:
            # Print the header line.
            print("\n-=-=-{Input}", end="")
            char = "-"
            for n in range(12, line_length):
                print(char, end="")
                if char == "-":
                    char = "="
                else:
                    char = "-"
                # end if
            # end for
            print()
            # If the user can quit or back out, print instructions.
            if quit_:
                wl_resource.print_nav(q=True, b=True)
                print("-" * line_length)
            # end if
            # Print the prompt and get a response.
            response = input(prompt + " [Y]/[N] >>  ")
            # Because the function uses an RE method, make sure that the
            #  response is compilable.  If its not, go straight to the
            #  error message.
            try:
                # If it's possible for the user to quit and he/she does
                #  so, just return that response.
                if quit_ and re.match(r"-(b|q)", response, re.I):
                    return response
                # Otherwise, return True for yes and False for no.
                elif re.match(r"y", response, re.I):
                    return True
                elif re.match(r"n", response, re.I):
                    return False
            except Exception:
                pass
            # end try.
            # If the response didn't match anything, print an error and
            #  loop back.
            else:
                print_status(
                  "Error", "That wasn't a 'yes' or a 'no'…",
                  line_length=line_length)
            # end if
        # end while
    except Exception as err:
        _z_exc("io_utils.py/yes_no", err)
    # end try
# end function


def _menu_build_display_list(
  options, option_type, prompt, keystroke, keystroke_list, line_length,
  multiple, quit_, top_level, header):
    """-----------------------------------------------------------------
        Builds the contents of a menu.

        Arguments:
        - options -- the list of options to display.
        - option_type -- a word or phrase describing the options, used
           only if prompt is an empty string.
        - prompt -- the menu prompt.
        - keystroke -- allow menu choices by keystroke.
        - keystroke_list -- a list of possible keystroke responses, or
           "#", signifying responses by number.
        - line_length -- the width of the screen in characters.
        - multiple -- allow multiple responses.
        - quit_ -- allows the user to quit.
        - top_level -- flag indicating a top-level menu.
        - header -- an optional header line.

        Returns:  a list of lines to be printed.
       -----------------------------------------------------------------
    """
    try:
            # Create a generic prompt if one hasn't been provided.
        if not prompt:
            pr_str = "Please select one "
            if multiple:
                pr_str += "or more "
            # end if
            prompt = pr_str + "of the following " + option_type + ":"
        # end if
        display_list = []
        # TODO:  Implement help screen.
        #
        # If the option(s) is/are to be chosen by number, prefix numbers
        #  to the options; if by keyboard shortcut, prefix shortcuts.
        #  Otherwise just transfer the options unchanged.
        if keystroke_list == "#":
            if quit_:
                if top_level:
                    display_list.append("[0] Quit\n" + ("-" * (line_length)))
                else:
                    display_list.append(
                      "[0] Go Back\n" + ("-" * (line_length)))
                # end if
            # end if
            if header:
                display_list.append(header[:line_length])
            # end if
            for n, option in enumerate(options):
                display_list.append(
                  "[" + str(n + 1) + "] " + option[:line_length - 4])
            # end for
        elif keystroke:
            if quit_:
                if top_level:
                    display_list.append("[Q] Quit\n" + ("-" * (line_length)))
                else:
                    display_list.append(
                      "[Q] Go Back\n" + ("-" * (line_length)))
                # end if
            # end if
            if header:
                display_list.append(header[:line_length])
            # end if
            for n, option in enumerate(options):
                display_list.append(
                  "[" + keystroke_list[n] + "] " + option[:line_length - 4])
            # end for
        else:
            if quit_:
                if top_level:
                    display_list.append("Quit\n" + ("-" * (line_length)))
                else:
                    display_list.append("Go Back\n" + ("-" * (line_length)))
                # end if
            # end if
            if header:
                display_list.append(header[:line_length])
            # end if
            for option in options:
                display_list.append(option[:line_length])
            # end for
        # end if
        # Finally, add bottom separator.
        display_list.append('-' * (line_length))
        return display_list
    except Exception as err:
        _z_exc("io_utils.py/_menu_build_display_list", err)
    # end try
# end function


def _menu_display(
  display_list, prompt, lines, multiple, nav, prev, nxt, line_length):
    """-----------------------------------------------------------------
        Displays a menu.

        Arguments:
        - display_list -- the list of options to display.
        - prompt -- the menu prompt.
        - lines -- print one option on each line.
        - multiple -- allow multiple responses.
        - nav - print navigation options.
        - prev - print "previous" option; ignored if nav is False.
        - nxt - print "next" option; ignored if nav is False.
        - line_length - width of the screen in characters.

        Returns:  nothing.
       -----------------------------------------------------------------
    """
    try:
        # Print the menu and get a response.
        print(
          "\n-=-=-{Input}", end="")
        char = "-"
        for n in range(12, line_length):
            print(char, end="")
            if char == "-":
                char = "="
            else:
                char = "-"
            # end if
        # end for
        print()
        # TODO:  Implement multi-column display.
        if len(prompt) < line_length:
            print(prompt, "\n")
        else:
            print_block(prompt)
            print()
        # end if
        for n, option in enumerate(display_list):
            if lines or (n == len(display_list) - 1):
                print(option)
            else:
                print(option, end=", ")
            # end if
        # end for
        if multiple:
            print("\nSeparate multiple choices with commas.")
        # end if
        # If necessary, print navigational options.
        if nav and (prev or nxt):
            print()
            if prev:
                print("[P] Previous  ", end="")
            # end if
            if nxt:
                print("[N] Next", end="")
            # end if
            print()
        # end if
        return
    except Exception as err:
        _z_exc("io_utils.py/_menu_display", err)
    # end try
# end function


def _menu_evaluate_response(
  response_list, options, keystroke, keystroke_list, multiple, validate_all,
  match_case, quit_, nav, help_toggle, line_length):
    """-----------------------------------------------------------------
        Evaluates the response to a menu.

        Arguments:
        - response_list -- the user's response.
        - options -- the list of options.
        - keystroke -- enable response by keystroke.
        - keystroke_list -- list of keystroke options, or "#",
           signifying selection by number.
        - multiple -- allows multiple responses.
        - validate_all -- requires all responses to be valid; ignored
           if multiple is False.
        - match_case -- requires responses to match the case of the
           options.
        - quit_ -- allows the user to quit/go back.
        - nav -- allows for navigational responses.
        - help_toggle -- allows for a response toggling help.
        - line_length -- the width of the screen in characters.

        Returns:
         if quit_ is True and the user chooses to quit, 0;
         if multiple is False, an 1-based integer representing the
          user's choice;
         if multiple is True, a list of 1-based integers representing
          the user's choices.
         if nav is True and the user so enters, "-p" or "-n";
         if help_toggle is True and the user so enters, "-h";
         if the user did not enter any valid choices, or if validate_all
          is True and and the user entered an invalid choice, None.
       -----------------------------------------------------------------
    """
    try:
        invalid_list = []
        # Check for navigational response.
        if nav and (response_list[0].lower() in ["p", "n"]):
            return response_list[0].lower()
        # end if
        # Check for help toggle.
        if help_toggle and (response_list[0].lower() == "-h"):
            return response_list[0].lower()
        # end if
        # Validate each choice.
        for n in range(len(response_list)):
            # Even if the menu presents options by number or
            #  keystroke, the user can always make a choice by
            #  typing the option itself (or just the beginning of
            #  the option).  But since this can conflict with
            #  numeric and keystroke entries, don't do this check if
            #  the response is only one character long.
            if len(response_list[n]) > 1:
                # Because this block uses regex methods, first make
                #  sure that the user input is compilable.  If it's
                #  not, skip this block entirely.
                try:
                    resp_ci = re.compile(response_list[n], re.I)
                    resp = re.compile(response_list[n])
                    # If the user can quit and that is his/her response,
                    #  return immediately (even if there are other
                    #  responses).  Note that for the quit option, the
                    #  match_case argument is ignored.
                    if quit_ and re.match(resp_ci, "quit"):
                        return 0
                    # end if
                    # Otherwise, the response has to match the
                    #  beginning of an option (possibly including
                    #  case).
                    for x in range(len(options)):
                        if match_case:
                            # If the response matches the beginning
                            #  of an option, replace the response
                            #  with the integer.
                            if re.match(resp_ci, options[x]):
                                response_list[n] = x + 1
                                break
                            # end if
                        else:
                            # Same, ignoring case.
                            if re.match(resp, options[x]):
                                response_list[n] = x + 1
                                break
                            # end if
                        # end if
                    # end for
                    # If the response wasn't converted to an
                    #  integer, it didn't match anything.
                    if type(response_list[n]) != int:
                        invalid_list.append(response_list[n])
                        response_list[n] = "*"
                    # end if
                except Exception:
                    pass
                # end try
            # end if
            # For number choices, just make sure that it's a number
            #  and that it's within the range of options.
            elif keystroke_list == "#":
                try:
                    response_list[n] = int(response_list[n])
                except ValueError:
                    invalid_list.append(response_list[n])
                    response_list[n] = "*"
                    continue
                # end try
                # If the user can quit and that is his/her response,
                #  return immediately (even if there are other
                #  responses).
                if quit_ and response_list[n] == 0:
                    return 0
                else:
                    if response_list[n] > len(options):
                        invalid_list.append(response_list[n])
                        response_list[n] = "*"
                    # end if
                # end if
            # Keystroke responses need to be checked against the
            #  keystroke list.
            elif keystroke:
                # If the user can quit and the response is to quit,
                #  return immediately (even if there are other
                #  responses).  Note that for the quit option, the
                #  match_case argument is ignored.
                if quit_ and response_list[n].lower() == "q":
                    return 0
                # end if
                # Check if the response matches one of the options.
                for x in range(len(keystroke_list)):
                    if match_case:
                        # If the response matches the option,
                        #  replace the response with the integer.
                        if response_list[n] == keystroke_list[x]:
                            response_list[n] = x + 1
                            break
                        # end if
                    else:
                        # Same, ignoring case.
                        if (
                          response_list[n].lower() ==
                          keystroke_list[x].lower()):
                            response_list[n] = x + 1
                            break
                        # end if
                    # end if
                # end for
                # If the response wasn't converted to an integer, it
                #  didn't match anything.
                if type(response_list[n]) != int:
                    invalid_list.append(response_list[n])
                    response_list[n] = "*"
                # end if
            # end if
        # end for
        # If there were invalid responses, remove the "*"s from the
        #  response list.
        if invalid_list:
            for n in range(len(response_list) - 1, -1, -1):
                if response_list[n] == "*":
                    response_list.pop(n)
                # end if
            # end for
        # end if
        # TODO:  Implement confirm block.
        #
        # If validate_all is True, the response is not valid if any
        #  choice is invalid.  Otherwise, only return the valid
        #  choice(s).
        # But if ALL the choices were invalid, do not return.
        if (not validate_all) and (response_list):
            # If multiple is True, return a list (even if it has
            #  only one element).  If multiple is False, return only
            #  the first element (even if there are others).
            if multiple:
                return response_list
            else:
                return response_list[0]
            # end if
        else:
            # Build the error message.
            if len(invalid_list) == 1:
                err_msg = str(invalid_list[0]) + " is not a valid option."
            else:
                err_msg = str_utils.comma_str_from_list(
                  invalid_list) + " are not valid options."
            # end if
            # Print error message.
            print_status("Error", err_msg, line_length=line_length)
            return None
        # end if
    # end while
    except Exception as err:
        _z_exc("io_utils.py/_menu_evaluate_response", err)
    # end try
# end function


def _menu_get_response(line_length):
    """-----------------------------------------------------------------
        Gets a user's response to a menu.

        Arguments:
        - line_length - the width of the screen in characters.

        Returns:  the user's response, or None if the user didn't enter
         anything.
       -----------------------------------------------------------------
    """
    try:
        # Get input from the user, and split it into individual
        #  items (if more than one choice is entered).
        response_list = re.split(r",\s*", input("\n>>  "))
        # If the user didn't enter anything, try again.
        if response_list == [""]:
            print_status(
              "Error", "You did not enter anything.",
              line_length=line_length)
            return None
        # end if
        return response_list
    except Exception as err:
        _z_exc("io_utils.py/_menu_get_response", err)
    # end try
# end function
