"""---------------------------------------------------------------------
This module handles basic file input and output.

   ---------------------------------------------------------------------
"""

import os
import csv

import io_utils
import wl_resource


def file_create(filetype="txt"):
    """-----------------------------------------------------------------
        Creates a new file to store data.  Offers to overwrite an
         existing file.

        Arguments:  none.

        Returns:  The name of the file created, or an empty string if
         unsuccessful; and a bool, which is True only if the named file
         exists and the user wants to open it.
       -----------------------------------------------------------------
    """
    fname = ""
    while not fname:
        fname = input("Please enter a name for the new file:  ")
        if not fname:
            # If the user entered nothing, ask if they want to go
            #  back.
            exit = io_utils.yes_no(
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
                wl_resource.print_status(
                  "warning", msg=f"{fname} already exists.", go=True)
                choice = io_utils.menu(
                        ["Open this file.", "Replace this file",
                         "Create a new file with a different name"],
                         confirm=True, keystroke=True,
                         keystroke_list=["O", "R", "C"])
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
                    exit = io_utils.yes_no("Do you want to try again?")
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


def file_open(fname= "", filetype="txt"):
    """-----------------------------------------------------------------
        Opens and reads a file.

        Keyword arguments:
        - fname -- the name of the file to open.
        - filetype -- the extension of the file to open or create
           (default txt).

        Returns:  A tuple consisting of the name of the file selected,
         and a data element.  If opening a file, the data element will
         be:  for a txt file, a list containing the lines of text in the
         file; for a csv file, a list of dictionaries containing the
         data in the file.  If the open or read operations failed, the

       -----------------------------------------------------------------
    """
    # If the caller didn't pass a filename, get one.
    if not fname:
        fname = get_filename_open(filetype)
    # end if
    # If we have a filename, go open and read it.
    if fname:
        success, data_list = _open_read(fname, filetype)
        if success:
            return fname, data_list
        else:
            return "", []
        # end if
    else:
        # If the user decided to quit (or if there are no files that can
        #  be opened), go back to the previous menu.
        return "", []
    # end if
# end function


def file_write(fname, filetype, data_list, fieldnames=None):
    """-----------------------------------------------------------------
        This internal function opens a file and writes data to it.

        Arguments:
        - fname -- the name of the file to open.
        - filetype -- the type of file (the function does not check to
            ensure that the file type matches the extension).

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
                # end for
            # end if
        # end with
    except:
        wl_resource.print_status("error", msg="Error writing log file.")
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
        print("Enter the name of the file you want to open, or [?] to")
        print("see a list of available files.")
        fname = input("Enter [Q] to go back:  ")
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
                  "status", msg="Sorry, no available files found.")
                fname = ""
                valid = True
            else:
                for f in files:
                    # remove any files of the wrong filetype.
                    if f[-3:] != filetype:
                        files.remove(f)
                    # end if
                # end for
                # If no files of the right filetype were found, go back
                #  to the previous menu.
                if len(files) == 0:
                    wl_resource.print_status(
                      "status", msg="Sorry, no available files found.")
                    fname = ""
                    valid = True
                else:
                    # Show a menu of the available files, keyed by
                    #  number.
                    choice = io_utils.menu(
                        files, option_type="files", keystroke=True,
                        keystroke_list=["#"], lines=True)
                    if choice:
                        fname = fname[choice - 1]
                        valid = True
                # end if
            # end if
        # end if
    # end while
    return fname
# end function


def _open_read(fname, filetype):
    """-----------------------------------------------------------------
        This internal function opens a given file and retrieves the data
         inside it.

        Arguments:
        - fname -- the name of the file to open.
        - filetype -- the type of file (the function does not check to
            ensure that the file type matches the extension).

        Returns:  A tuple consisting of a bool indicating whether or
         not the function succeeded, and a data element.  The contents
         of the data element depend on the type of file read.
       -----------------------------------------------------------------
    """
    try:
        with open(fname, "r", newline="") as data_file:
            if filetype == "txt":
                data_list = list(data_file)
            elif filetype == "csv":
                data_list = list(
                        csv.DictReader(data_file, delimiter=","))
            else:
                # If the file type doesn't match any known type, return
                #  an error.
                wl_resource.print_status(
                  "error", msg="Unrecognized file type.")
                return False, []
            # end if
            return True, data_list
        # end with
    except:
        wl_resource.print_status(
          "error", msg=f"An error occured while reading {fname}.")
        return False, []
    # end try
# end function
