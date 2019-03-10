import csv
import os
import re

import str_utils
import wl_resource


"""---------------------------------------------------------------------
    Contains i/o-related functions.
   ---------------------------------------------------------------------
"""

def build_dict_string(dic):
    """-----------------------------------------------------------------
        Builds and returns a string representation of a dictionary.

        Arguments:
        - dic -- the dictionary to process.

        Returns:  the string representing the dictionary.
       -----------------------------------------------------------------
    """
    # Why to build a string representation piecemeal instead of just
    #  using str:  The str method, when used on a whole dictionary (as
    #  opposed to a specific value), returns the __repr__ of each value,
    #  rather than the __str__.  For built-in types these two values are
    #  the same, but for other objects (notably datetime objects) they
    #  may not be.
    #
    # If the function is passed an empty dictionary, just return the
    #  string representation of that.
    if not dic:
        return "None"
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
# end function


def clear_screen():
    """-----------------------------------------------------------------
        Clears the screen.

        Arguments:  None.

        Returns:  Nothing.
       -----------------------------------------------------------------
    """
    # This print line is a marker for those terminals/shells which
    #  refuse to implement the system call.  For those terminals/shells
    #  that do, this line will instantly disappear.
    print(
      "SCREENCLEARSHERE SCREENCLEARSHERE SCREENCLEARSHERE SCREENCLEARSHERE")
    os.system("cls" if os.name == "nt" else "clear")
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
    d = 0
    # Loop through the list backwards.
    for n in range(len(lst)-1, -1, -1):
        # If the item matches, delete it.
        if index != None:
            if lst[n][index] in condition:
                del lst[n]
                d += 1
            # end if
        elif attr != None:
            if getattr(lst[n], attr) in condition:
                del lst[n]
                d += 1
        elif lst[n] in condition:
            del lst[n]
            d += 1
        # end if
    # end for
    return d
# end function


def confirm(prompt):
    """-----------------------------------------------------------------
        Asks the user to confirm a decision.

        Arguments:
        - prompt -- descriptive text of what ot confirm.

        Returns:  True if the user confirms, otherwise False.
       -----------------------------------------------------------------
    """
    # Unlike the yes_no function, confirm doesn't loop seeking a valid
    #  answer.  It treats "Y" (or "y") as confirmation, and any other
    #  input as non-confirmation.
    print(
      "\n-=-=-{Confirm}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
      "=-=-")
    response = input(
      print_block("Are you sure you want to " + prompt + "? [Y/N]:  ",
      lf=False, ret_str=True))
    if re.match(r"y", response, re.I):
        return True
    else:
        return False
    # end if
# end function


def file_create(filetype="txt"):
    """-----------------------------------------------------------------
        Creates a new file to store data.  Offers to overwrite an
         existing file.

        Keyword Arguments:
        - filetype -- the type of file to create (default "txt").

        Returns:  The name of the file created, or an empty string if
         unsuccessful; and a bool, which is True only if the named file
         exists and the user wants to open it.
       -----------------------------------------------------------------
    """
    fname = ""
    while not fname:
        fname = get_input(prompt="Please enter a name for the new file:")
        if not fname:
            # If the user entered nothing, ask if they want to go
            #  back.
            exit = yes_no("You did not enter a name.  Do you want to go back?")
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
                wl_resource.print_status(
                  "warning", msg=f"{fname} already exists.", go=True)
                choice = menu(
                        ["Open this file.", "Replace this file",
                         "Create a new file with a different name"],
                         confirm=True, keystroke=True,
                         keystroke_list=["O", "R", "C"], lines=True)
                # If the user chose to quit, return an empty string.
                if choice == 0:
                    return "", False
                elif choice == 1:
                        # The user chose to open this file.  Return the
                        #  filename and flag to open the file.
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
                except:
                    print("An error occured while creating the file.")
                    # Ask the user if they want to try again or go
                    #  back.
                    exit = yes_no("Do you want to try again?")
                    if exit:
                        # User wants to exit.
                        return "", False
                    else:
                        # Loop back to getting a filename.
                        continue
                    # end if
                # end try
            # end if
        # end if
    # end while
    # Unless something went wrong along the way, return the file name.
    return fname, False
# end function


def file_read(fname, filetype="txt"):
    """-----------------------------------------------------------------
        Opens and reads a file.

        Arguments:
        - fname -- the name of the file to open.

        Keyword Arguments:
        - filetype -- the extension of the file to open or create
           (default txt).

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
                wl_resource.print_status(
                  "error", msg="Unrecognized file type.")
                return []
            # end if
            return data_list
        # end with
    except:
        wl_resource.print_status(
          "error", msg="An error occured while reading the file.")
        return []
    # end try
# end function


def file_write(fname, filetype, data_list, fieldnames=None):
    """-----------------------------------------------------------------
        Opens a file and writes data to it.

        Arguments:
        - fname -- the name of the file to open.
        - filetype -- the type of file (the function does not check to
            ensure that the file type matches the extension).

        Keyword Arguments:
        - fieldnames -- for csv files, the field names of the dictionary
           to be written.

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
        wl_resource.print_status(
          "warning", msg=f"Error writing log file:  {err}")
        return False
    # end try
    return True
# end function


def get_filename_open(filetype):
    """-----------------------------------------------------------------
        Gets the name of a file to open.  On request, displays a list of
         files in the working directory and allows the user to choose
         one.

        Arguments:
        - filetype -- extension of the file to open.

        Returns:  the name of the file to open.
       -----------------------------------------------------------------
    """
    valid = False
    while not valid:
        prompt = (
          "Enter the name of the file you want to open, or [?] to see a " +
          "list of available files.  Enter [Q] to go back:")
        fname = get_input(prompt=prompt)
        if fname.upper() == "Q":
            # If the user backs out, set the filename to an empty string
            #  and set the loop to end.
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
                wl_resource.print_status(
                  "error", msg=f"File {fname} not found.")
        else:
            # Scan the directory and present a menu of available
            #  files.
            files = os.listdir()
            if not files:
                # If there were no files in the directory, go back to
                #  the previous menu.
                wl_resource.print_status(
                  "warning", msg="No available files found.")
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
                # If no files of the right filetype were found, go back
                #  to the previous menu.
                if len(files) == 0:
                    wl_resource.print_status(
                      "warning", msg="No available files found.")
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
    # end while
    return fname
# end function


def get_input(prompt, typ="str"):
    """-----------------------------------------------------------------
        Prompts for input from the user.

        Arguments:
        - prompt -- the prompt to display (default ">>").

        Keyword arguments:
        - typ -- the type of input to return (default "str").

        Returns:  a string with the user's input; None if a specific
         type is required and the user's input cannot be converted to
         that type.
       -----------------------------------------------------------------
    """
    # Print the header line.
    print(
      "\n-=-=-{Input}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
      "=-=-")
    # Get the user's input.
    response = input(print_block(prompt, lf=False, ret_str=True) + "  ")
    # If the caller wants a string, just return.
    if typ == "str":
        return response
    # end if
    # If the caller wants a different built-in type, try to convert the
    #  response, and return None if there is an exception.
    try:
        if type == "int":
            response = int(response)
            return response
        elif type == "float":
            response = float(response)
            return response
        # end if
    except ValueError:
        return None
    # end try
    # If the type wasn't recognized, just return the raw input.
    return response
    # end if
# end function


def menu(options, option_type="options", confirm=False, keystroke=False,
  keystroke_list=[], match_case=False, multiple=False, lines=True,
  columns=1, col_dir="down", validate_all=False, show_help=False,
  help_text="", top_level=False, prompt="", quit=True, nav=False,
  prev=False, nxt=False, header=""):
    """-------------------------------------------------------------
        Presents a menu and obtains a response from the user.

        Arguments:
        - options -- list of options from which to choose.

        Keyword Arguments:
        - option_type -- word or phrase describing the options (default
           "options").
        - confirm -- asks the user to confirm his/her choice(s) before
           returning (default False).
        - keystroke -- specifies selection by shortcut (default False).
        - keystroke_list -- list of shortcuts corresponding to the
           options; ignored if keystroke is False, unless it is "#",
           which specifies selection by number (default empty list).
           (NOTE:  "Q" is reserved for the quit option and cannot be
           included in the list).
        - match_case -- requires the user's response(s) to match the
           case of the option(s).
        - multiple -- allows the selection of multiple options (default
           False).
        - lines -- print each option on a separate line; ignored if
           columns > 1 (default True).
        - columns -- number of columns in which to arrange the options;
           can be 1 to 3 (default 1).
        - col_dir -- direction in which to arrange the options in a
           multi-column display; ignored if columns = 1 (default
           "down").
        - validate_all -- requires all choices made by the user to be
           valid options (defualt False)
        - show_help -- allows the user to choose to see a help screen
           before making his/her choice(s) (default False).
        - help_text -- the help text to show the user; ignored if
           show_text is False (default empty string).
        - top_level -- flag indicating a top-level menu (default False).
        - prompt -- the prompt to display (default empty string).
        - quit -- allows the user to quit/abort/go back (default True).
        - nav -- prints additional navigational choices (ignored unless
           the menu choices are numbered) (default False).
        - prev -- prints the choice to move backards (ignored if nav is
           False) (default False).
        - nxt -- prints the choice to move forwards (ignored if nav is
           False) (default False).
        - header -- print a header line before the first option (but
           after the quit option, if quit is True (default empty
           string).

        Returns:  if multiple is True, a list of integers corresponding
         to the choice(s) made; if multiple is False, a single integer.
         NOTE that "quit" is returned as 0; other choices are 1-based.
         If nav is True, may also return "-p" or "-n".
       -------------------------------------------------------------
    """
    # Make sure the column argument is valid.
    if not (0 < columns <= 3):
        columns = 1
    # end if
    # Disable nav unless the menu choices are numbered.
    if keystroke_list != "#":
        nav = False
    # end if
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
    # If the option(s) is/are to be chosen by number, prefix numbers
    #  to the options; if by keyboard shortcut, prefix shortcuts.
    #  Otherwise just transfer the options unchanged.
    if keystroke_list == "#":
        if quit:
            if top_level:
                display_list.append("[0] Quit\n" + ("-" * 69))
            else:
                display_list.append("[0] Go Back\n" + ("-" * 69))
            # end if
        # end if
        if header:
            display_list.append(header)
        # end if
        for n, option in enumerate(options):
            display_list.append("[" + str(n + 1) + "] " + option)
        # end for
    elif keystroke:
        if quit:
            if top_level:
                display_list.append("[Q] Quit\n" + ("-" * 69))
            else:
                display_list.append("[Q] Go Back\n" + ("-" * 69))
            # end if
        # end if
        if header:
            display_list.append(header)
        # end if
        for n, option in enumerate(options):
            display_list.append(
              "[" + keystroke_list[n] + "] " + option)
        # end for
    else:
        if quit:
            if top_level:
                display_list.append("Quit\n" + ("-" * 69))
            else:
                display_list.append("Go Back\n" + ("-" * 69))
            # end if
        # end if
        if header:
            display_list.append(header)
        # end if
        for option in options:
            display_list.append(option)
        # end for
    # end if
    # Run this part in a loop until a valid response is entered.
    while True:
        invalid_list = []
        # Print the menu and get a response.
        print(
          "\n-=-=-{Input}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
        # TODO:  Implement multi-column display.
        if len(prompt) < 80:
            print(prompt)
        else:
            print_block(prompt)
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
        # Get input from the user, and split it into individual
        #  items (if more than one choice is entered).
        response_list = re.split(r",\s*", input("\n>>  "))
        # If the user didn't enter anything, try again.
        if not response_list:
            wl_resource.print_status(
              "error", msg="You did not enter anything.")
            input("Press [ENTER] to continue.")
            continue
        # end if
        # Check for navigational response.
        if nav and (response_list[0].lower() in ["p", "n"]):
            return response_list[0].lower()
        # end if
        # Validate each choice.
        for n in range(len(response_list)):
            # For number choices, just make sure that it's a number
            #  and that it's within the range of options.
            if keystroke_list == "#":
                try:
                    response_list[n] = int(response_list[n])
                except ValueError:
                    invalid_list.append(response_list[n])
                    response_list[n] = "*"
                    continue
                # end try
                # If the response is to quit, return immediately
                #  (even if there are other responses).
                if response_list[n] == 0:
                    return 0
                else:
                    if response_list[n] > len(options):
                        invalid_list.append(response_list[n])
                        response_list[n] = "*"
                    # end if
                # end if
            elif keystroke:
                # If the response is to quit, return immediately
                #  (even if there are other responses).  Note that
                #  for the quit option, the match_case attribute is
                #  ignored.
                if response_list[n].lower() == "q":
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
            else:
                # If the response is to quit, return immediately
                #  (even if there are other responses).  Note that
                #  for the quit option, the match_case attribute is
                #  ignored.
                if response_list[n].lower() == "quit":
                    return 0
                # end if
                # Otherwise, the response has to match an option
                #  exactly (except possibly for case).
                for x in range(len(keystroke_list)):
                    if match_case:
                        # If the response matches the option,
                        #  replace the response with the integer.
                        if response_list[n] == options[x]:
                            response_list[n] = x + 1
                            break
                        # end if
                    else:
                        # Same, ignoring case.
                        if (
                          response_list[n].lower() ==
                          options.lower()):
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
        # If validate_all is True, the response is not valid if any
        #  choice is invalid.  Otherwise, just return the valid
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
            err_msg = ""
            if len(invalid_list) == 1:
                err_msg = invalid_list[0] + " is not a valid option."
            else:
                err_msg = str_utils.comma_str_from_list(
                  invalid_list) + " are not valid options."
            # end if
            print(
              "\n-=-=-{Error}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
              "=-=-=-=-")
            print(err_msg)
            input("Press [ENTER] to continue.")
            continue
        # end if
    # end while
    # Dummy return (if the method reaches this line something went
    #  wrong).
    return -1
# end function


def print_block(string, length=70, lf=True, ret_str=False):
    """-----------------------------------------------------------------
        Takes a long string and prints it within a specified width.

        Arguments:
        - string -- the string to print.

        Keyword Arguments:
        - length -- the desired line length (default 80).
        - lf -- print a line feed after the block (default True)
        - ret_str -- flag to return a string rather than print it.

        Returns:  if string is True, a formatted string; else nothing.
       -----------------------------------------------------------------
    """
    if ret_str:
        r_str = ""
    # end if
    # Break the string into words, along spaces, hyphens, and newlines.
    word_list = re.split(r"(\s)|(-)|(¤)", string)
    col = 0
    for word in word_list:
        # Filter out None.
        if word:
            # If the word is a newline character, always print (or add)
            #  a new line, and reset the column counter.
            if word == "¤":
                if ret_str:
                    r_str += "\n"
                else:
                    print()
                # end if
                col = 0
            # If there is EXACTLY one character left on the line--
            elif col == length - 1:
                # If the word is a space or a hyphen, print or add it,
                #  and then a new line, and reset the column counter.
                if word in [" ", "-"]:
                    if ret_str:
                        r_str += word + "\n"
                    else:
                        print(word)
                    # end if
                    col = 0
                # If the word is anything else, print or add a new line,
                #  then the word, and reset the column counter.
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
                # Print or add the word if it won't run past the end of
                #  the line, and increment the column counter.
                if col + len(word) < length:
                    if ret_str:
                        r_str += word
                    else:
                        print(word, end="")
                    # end if
                    col += len(word)
                # If it would run past the end of the line, print or add
                #  a new line, then the word, and reset the column
                #  counter.
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
# end function


def welcome_screen(project_no, project_name):
    """-----------------------------------------------------------------
        Clears the screen and prints introductory text.

        Arguments: None

        Returns:  Nothing
       -----------------------------------------------------------------
    """
    clear_screen()
    print(
      "-=-=-{Welcome}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(
      "Treehouse Python Techdegree Project #" +
      str(project_no) + ":")
    print(project_name)
    print("-" * 69)
    print("Implemented by Steven Tagawa")
    print(
      "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    return
# end function


def yes_no(prompt, clear=False, quit=False):
    """-----------------------------------------------------------------
        Prompts the user to answer a yes or no question.

        Arguments:
        - prompt -- The question to be answered.

        Keyword arguments:
        - clear -- Clear the screen first (default False).
        - quit -- Allow the user to go back or quit (default False).

        Returns:  True if the user answers yes, False if no.  If quit is
         True, will also return "-b" or "-q" if the user enters it.
       -----------------------------------------------------------------
    """
    # Clear the screen if applicable.
    if clear:
        clear_screen()
    # Run in a loop until a valid response is obtained.
    while True:
        print(
          "\n-=-=-{Input}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-")
        if quit:
            wl_resource.print_nav(q=True, b=True)
            print("-" * 69)
        # end if
        response = input(prompt + " [Y]/[N]>>  ")
        if quit and re.match(r"-(b|q)", response, re.I):
            return response
        elif re.match(r"y", response, re.I):
            return True
        elif re.match(r"n", response, re.I):
            return False
        else:
            wl_resource.print_status(
              "error", msg="That wasn't a 'yes' or a 'no'...")
        # end if
    # end while
# end function


