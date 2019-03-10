# Imports.
import re
import io_utils

class WlHelp:

    """-----------------------------------------------------------------
        Object which handles help strings for the work log script.
       -----------------------------------------------------------------
    """

    help_list = {}

    def __init__(self):
        self._load_help()

    def print_help(self, show_help, title, label, format_list=[]):
        """-------------------------------------------------------------
            Prints a help string.

            Arguments:
            - show_help -- the help flag.
            - label -- the identifier of the help string to print.
            - title -- the help subject to print.

            Keyword arguments:
            - format_list -- list of values to insert for placeholders
               in the help string.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        # Get the specified help entry.
        help_entry = self.help_list[label]
        # Print the top separator line.
        print(
          "-=-=-{Info/Help}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
          "=-=-=-=-")
        # If help is turned on, print the help string, and instructions
        #  to turn help off.
        if show_help:
            print(title, "\n" + ("-" * 69))
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
                io_utils.print_block(help_entry, length=70)
            # Otherwise just print the help entry.
            else:
                io_utils.print_block(help_entry, length=70)
            # end if
            print("-" * 69, "\nEnter [-h] to hide help.")
        # Otherwise, print instructions to turn help on.
        else:
            print("Enter [-h] to show help.")
        # Print the bottom separator line.
        print(
          "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
          "-=-")
        return
    # end method

    def _load_help(self):
        """-------------------------------------------------------------
            Loads help text strings from an external file, "help.txt".

            Arguments:  none

            Returns:  nothing
           -------------------------------------------------------------
        """
        # Open the help text file.
        try:
            with open("help.txt", newline="") as file:
                # Read the entire file into a temporary list.
                input_list = file.readlines()
            # end with
        except:
            print("Error loading help text.")
        # end try
        # Discard the first line.
        del input_list[0]
        # Read through the list, concatenating each help string and
        #  adding it to the help object dictionary.
        for line_no, line in enumerate(input_list):
            # Title lines begin with an underscore.
            if line[0] == "_":
                # Title lines contain the help entry title and the
                #  number of lines the entry takes.  The simplest way
                #  to process this is to break the line at the comma.
                temp_list = line.split(", ")
                # The entry's key in the help dictionary is the first
                #  element.
                help_key = temp_list[0]
                # The second element is how many lines to read.  (The
                #  entry starts on the next line, so the index is 1-
                #  based.)
                help_entry = ""
                for x in range(1, int(temp_list[1]) + 1):
                    help_entry += input_list[line_no + x][:-2] + " "
                # end for
                # Set the key and value in the help dictionary.
                self.help_list[help_key] = help_entry
            # end if (the loop will skip to the next title line)
        # end for
        return
    # end method
