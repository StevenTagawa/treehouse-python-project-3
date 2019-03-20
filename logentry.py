"""---------------------------------------------------------------------
    Contains the specification of a LogEntry object, which is an object
     containing information on a single task within the WorkLog object.

    Class Definitions:
    - LogEntry -- the log entry object.

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
    import random

    import io_utils
    import str_utils
    import wl_resource
except Exception as err:
    _z_exc("logentry.py/module imports", err)
# end try


class LogEntry:
    """-----------------------------------------------------------------
        A log entry object.

        Attributes:
        - id -- the object's identifier, a random nine-digit integer.
           (Not guaranteed to be unique, but the odds of duplication are
           low enough to be acceptable for this program.)
        - title -- the title assigned to the task.
        - date -- a date object; the date of the task.
        - time -- a time object; the start time of the task.
        - datetime -- a datetime object obtained by combining the date
           and time attributes; used internally and not exposed to the
           user.
        - duration-- a timedelta object; the time spent on the task.
        - notes -- optional note for the task.
        - recurring -- flag indicating whether the task should recur at
           a specified interval.
        - rec_interval -- a dictionary containing flags which govern the
           interval at which the task recurs; empty if recurring is
           False.
        - rec_total -- the number of times the task recurs (not
           including the original task).
        - rec_child_seq -- a tuple denoting the task's place in a
           recurring sequence of tasks.  None if the task is not part of
           a sequence.
        - rec_parent -- the id attribute of the original task.  None if
           the task is not part of a sequence.
        - info -- a dictionary that serves as an internal holding area
           for data.

        Public Methods:
        - from_dict -- initializes the object's attributes using the
           values in a dictionary that has been created from reading a
           file.
        - to_dict -- exports the values of the object's attributes to a
           dictionary, which can be written to a file.

        Magic Methods:
        - __init__ -- creates an empty log entry object.
        - __eq__ -- overrides the = operator to allow object comparison.
       -----------------------------------------------------------------
    """
    FIELDNAMES = [
      "id", "title", "date", "time", "datetime", "duration", "notes",
      "recurring", "rec_interval", "rec_total", "rec_child_seq", "rec_parent",
      "info"]

    def __init__(self):
        """Initialization method.  Returns an empty log entry object."""
        self.id = random.randint(0, 1 * (10 ** 9))
        self.title = None
        self.date = None
        self.time = None
        self.datetime = None
        self.duration = None
        self.notes = None
        self.recurring = None
        self.rec_interval = {
          "unit": None, "skip": None, "days": None, "ordinal": None,
          "dates": None, "end": None}
        self.rec_total = None
        self.rec_child_seq = None
        self.rec_parent = None
        self.info = {}
    # end method

    def __eq__(self, other):
        """-------------------------------------------------------------
            Override the equality operator to allow work log objects to
             be compared.
           -------------------------------------------------------------
        """
        return self.__dict__ == other.__dict__
    # end method

    def from_dict(self, dict_entry, line_length=80):
        """-------------------------------------------------------------
            Converts a dictionary containing a log entry into a log
             entry object.

            Arguments:
            - dict_entry -- a dictionary containing log entry info.

            Keyword Arguments:
            - line_length -- the screen width in characters.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        try:
            # Set the entry object's attributes to the corresponding
            #  values in the dictionary entry.  Type conversions need to
            #  be done for non-string attributes.
            for key in dict_entry:
                # Don't do any of this if the string is empty or None.
                if not dict_entry[key]:
                    continue
                elif dict_entry[key][0] in ["(", "[", "{"]:
                    dict_entry[key] = (
                      str_utils.str_to_container(dict_entry[key]))
                else:
                    dict_entry[key] = str_utils.str_to_num(dict_entry[key])
                    dict_entry[key] = (
                      str_utils.str_to_datetime(dict_entry[key]))
                    dict_entry[key] = str_utils.str_to_bool(dict_entry[key])
                # end if
            # end for
            # Go through the attributes and set them.
            try:
                for attr in self.FIELDNAMES:
                    setattr(self, attr, dict_entry[attr])
                # end for
            except Exception as err:
                wl_resource.print_status(
                  "Error", f"Error creating entry:  {err}",
                  line_length=line_length)
            # end try
            return
        except Exception as err:
            _z_exc("logentry.py/from_dict", err)
        # end try
    # end method

    def to_dict(self):
        """-------------------------------------------------------------
            Creates a dictionary of strings with information from a log
             entry object.

            Arguments:  none.

            Returns:  a dictionary with the log entry object info.
           -------------------------------------------------------------
        """
        try:
            # Create the dictionary, converting each attribute to a
            #  string.
            dict_entry = {}
            dict_entry["id"] = str(self.id)
            dict_entry["title"] = str(self.title)
            dict_entry["date"] = str(self.date)
            dict_entry["time"] = str(self.time)
            dict_entry["datetime"] = str(self.datetime)
            dict_entry["duration"] = str(self.duration)
            dict_entry["notes"] = str(self.notes)
            dict_entry["recurring"] = str(self.recurring)
            dict_entry["rec_interval"] = (
              io_utils.build_dict_string(self.rec_interval))
            dict_entry["rec_total"] = str(self.rec_total)
            dict_entry["rec_child_seq"] = str(self.rec_child_seq)
            dict_entry["rec_parent"] = str(self.rec_parent)
            dict_entry["info"] = io_utils.build_dict_string(self.info)
            return dict_entry
        except Exception as err:
            _z_exc("logentry.py/to_dict", err)
        # end try
    # end method
# end class
