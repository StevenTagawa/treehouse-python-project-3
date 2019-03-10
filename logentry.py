import random

import io_utils
import str_utils
import wl_resource


class LogEntry:
    """-----------------------------------------------------------------
        A log entry object.
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

    def from_dict(self, dict_entry):
        """-------------------------------------------------------------
            Converts a dictionary containing a log entry into a log
             entry object.

            Arguments:
            - dict_entry -- a dictionary containing log entry info.

            Returns:  nothing.
           -------------------------------------------------------------
        """
        # Set the entry object's attributes to the corresponding values
        #  in the dictionary entry.  Type conversions need to be done
        #  for non-string attributes.
        for key in dict_entry:
            # Don't do any of this if the string is empty or None.
            if not dict_entry[key]:
                continue
            elif dict_entry[key][0] in ["(", "[", "{"]:
                dict_entry[key] = str_utils.str_to_container(dict_entry[key])
            else:
                dict_entry[key] = str_utils.str_to_num(dict_entry[key])
                dict_entry[key] = str_utils.str_to_datetime(dict_entry[key])
                dict_entry[key] = str_utils.str_to_bool(dict_entry[key])
            # end if
        # end for
        # Go through the attributes and set them.
        try:
            for attr in self.FIELDNAMES:
                setattr(self, attr, dict_entry[attr])
            # end for
        except:
            wl_resource.print_status("error", msg="Error creating entry.")
        # end try
        return
    # end method

    def to_dict(self):
        """-------------------------------------------------------------
            Creates a dictionary of strings with information from a log
             entry object.

            Arguments:  none.

            Returns:  a dictionary with the log entry object info.
           -------------------------------------------------------------
        """
        # Create the dictionary, converting each attribute to a string.
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
    # end method
