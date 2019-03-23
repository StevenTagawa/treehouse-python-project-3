"""
    Contains the specification for the work log's help object.

    Class Definitions:
    - WlHelp -- the work log help object.

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
    print("An interal error occurred in " + loc + ": ", err)
    # Exit.
    sys.exit(
      "Please report the above error and the circumstances which caused it " +
      "to the developer.")
    return  # Superfluous return.
# end function


# Other imports.
try:
    import re
    import io_utils
except Exception as err:
    _z_exc("wl_help.py/module imports", err)
# end try


class WlHelp:
    """
        Object which handles help strings for the work log script.

        Attributes:
        - help_list -- a list of help strings.

        Public Methods:
        - print_help -- prints a specified help string.

        Private Methods:
        - _load_help -- initializes the help_list attribute from a file.

        Magic Methods:
        - __init__ -- initalizes the help object via _load_help.
       -----------------------------------------------------------------
    """

    help_list = {}

    def __init__(self):
        self._load_help()

    def print_help(
      self, show_help, title, label, format_list=[], line_length=80):
        """
            Prints a help string.

            Arguments:
            - show_help -- the help flag.
            - label -- the identifier of the help string to print.
            - title -- the help subject to print.
            - line_length -- the width of the screen in characters
               (default 80).

            Keyword arguments:
            - format_list -- list of values to insert for placeholders
               in the help string.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            # Get the specified help entry.
            help_entry = self.help_list[label]
            # Print the header line.
            print("\n-=-=-{Info/Help}", end="")
            char = "-"
            for n in range(16, line_length):
                print(char, end="")
                if char == "-":
                    char = "="
                else:
                    char = "-"
                # end if
            # end for
            print()
            # If help is turned on, print the help string, and instructions
            #  to turn help off.
            if show_help:
                print(title, "\n" + ("-" * line_length))
                # Check if there are substitutions to be made.
                if format_list:
                    # Go through each value and insert it.
                    p = re.compile("«»")
                    for item in format_list:
                        # Replace the next placeholder in the help string
                        #  with the next value.
                        help_entry = p.sub(item, help_entry, count=1)
                    # end for
                    # Now print the modified entry.
                    io_utils.print_block(help_entry, line_length=line_length)
                # Otherwise just print the help entry.
                else:
                    io_utils.print_block(help_entry, line_length=line_length)
                # end if
                print("-" * line_length, "\nEnter [-h] to hide help.")
            # Otherwise, print instructions to turn help on.
            else:
                print("Enter [-h] to show help.")
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
            _z_exc("wl_help.py/WlHelp/print_help", err)
        # end try
    # end method

    def _load_help(self):
        """
            Loads help text strings from an external file, "help.txt".

            Arguments:  none

            Returns:  nothing
           -------------------------------------------------------------
        """
        try:
            # Open the help text file.
            try:
                with open("help.txt", newline="") as file:
                    # Read the entire file into a temporary list.
                    input_list = file.readlines()
                # end with
            except Exception as err:
                print(f"Error loading help text:  {err}")
            # end try
            # Discard the first line (because the beginning of the file can
            #  be corrupted, the first line is a dummy line).
            del input_list[0]
            # Clean-up:  this line is here for a particular IDE which
            #  doesn't like to import text files properly.
            for l in range(len(input_list)):
                input_list[l] = input_list[l].replace("Â", "")
            # end for
            # Read through the list, concatenating each help string and
            #  adding it to the help object dictionary.
            for l in range(len(input_list)):
                # Title lines begin with an underscore.
                if input_list[l][0] == "_":
                    # Title lines contain the help entry title and the
                    #  number of lines the entry takes.  The simplest way
                    #  to process this is to break the line at the comma.
                    temp_list = input_list[l].split(", ")
                    # The entry's key in the help dictionary is the first
                    #  element.
                    help_key = temp_list[0]
                    # The second element is how many lines to read.  (The
                    #  entry starts on the next line, so the index is 1-
                    #  based.)
                    help_entry = ""
                    for x in range(1, int(temp_list[1]) + 1):
                        help_entry += input_list[l + x][:-2] + " "
                    # end for
                    # Set the key and value in the help dictionary.
                    self.help_list[help_key] = help_entry
                # end if (the loop will skip to the next title line)
            # end for
            return
        except Exception as err:
            _z_exc("wl_help.py/WlHelp/_load_help", err)
        # end try
    # end method
# end class
