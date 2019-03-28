"""
    User manual for Treehouse Techdegree Project #3: Work Log
   ---------------------------------------------------------------------
"""

string = """
WORK LOG USER MANUAL

-------------------------------------------------------------------------------
CONTENTS:

  1.  Main Menu
  2.  Opening a File
  3.  Creating a File
  4.  Changing Settings
  4a.  Changing the Date Format
  4b.  Changing the Time Format
  4c.  Changing the Screen Width
  5.  Screen Header With Open File
  6.  Main Menu With Open File
  7.  Help With Open File
  8.  Adding an Entry
  8a.  Adding a Title
  8b.  Adding a Date
  8c.  Adding a Starting Time
  8d.  Adding a Duration
  8e.  Adding a Note
  8f.  Recurrance
  9.  Setting a Task Recurrance
  9a.  Choosing a Regular or Irregular Recurrance Interval
  9b.  Choosing a Recurrance Interval Type
  9c-1.  Choosing the Day(s) of Recurrance
  9c-2.  Choosing the Frequency of Recurrance
  9d-1.  Choosing Recurrance on Dates or Days During the Month
  9d-2a.  Choosing the Recurrance Dates
  9d-2b1.  Choosing the Recurrance Days
  9d-2b2.  Choosing the Weeks in Each Month for Recurrance
  9e.  Entering an End Date
  9f.  Confirming Recurrance Dates
  10.  Searching for Entries
  10a.  Searching by Date/Time
  10a-1.  Searching by a Single Date/Time
  10a-2.  Searching by a Range of Dates/Times
  10a-3.  Viewing All Dates
  10b.  Searching by Duration
  10c.  Searching by Text String
  10c-1.  Choosing Literal or Wildcard Search
  10d. Searching by RE Pattern
  11a.  Viewing All Results by Date
  11b.  Viewing Matching Results
  12.  Browsing Entries
  13.  Editing an Entry
  13a.  Making Changes to a Series of Entries
  14.  Deleting an Entry or a Series of Entries
  15.  Saving a File
  16.  Closing a File
  17.  Quitting the Program
  Appendix A.  Text Searching
  Appendix B.  Date Entry Formats
  Appendix C.  Time Entry Formats
  Appendix D.  Duration Entry Formats
-------------------------------------------------------------------------------

(NOTE:  In this manual, text to be inputted is surrounded by brackets [].  Do
not include the brackets when entering the text.)


  1.  Main Menu

Immediately after starting the program, you will see the main menu, which has
five options:
    • [Q] Quit
    • [O] Open log file
    • [N] New log file
    • [X] Settings
    • [M] Read User Manual

(NOTE:  In any menu which includes the option to quit or go back, that option
will always be the first chioce, and is always associated with the letter [Q]
(if the choices are lettered) or the number [0] (if the choices are numbered).
For this program, all menu choices are case-insensitive.)

Enter [O] to open an existing log file or [N] to create a new log file.  To
change the date format, time format, or number of characters that print across
the screen, enter [X].  To read this manual, enter [M].


  2.  Opening a File

After entering [O] at the main menu, you will be prompted to enter the name of
the file you want to open.  All Work Log data files are CSV files; but you do
not need to include the .csv extension when entering the file name.  To see a
menu of all CSV files in the current directory, enter [?].  You can then select
the name of the data file you want to open, or [0] to go back.  (The Work Log
program does not allow data files to be stored in a different directory.)

If you enter the name of a file that does not exist, or enter or select a csv
file that is not a valid Work Log data file, the program will let you know that
the file cannot be read, and return to the main menu.


  3.  Creating a File

After entering [N] at the main menu, you will be prompted to enter the name of
the file you want to create.  If you enter the name of a file that already
exists, you will be prompted to either:  1) open the file; 2) replace the file;
or 3) create a file with a different name.  You can also choose to go back to
the main menu.

(WARNING!!!  If you choose to replace an existing file, THE PROGRAM WILL
IMMEDIATELY OVERWRITE THE EXISING FILE WITH A NEW, BLANK FILE.  THIS CANNOT BE
UNDONE!)


  4.  Changing Settings

There are three settings that can be changed from this menu:
    • Date Format
    • Time Format
    • Screen Width


  4a.  Changing the Date Format

There are three date formats:
    • MM/DD/YY - known as "middle-endian", used in the U.S.
    • DD/MM/YY - known as "little-endian", used in Europe and Australia
    • YY/MM/DD - known as "big-endian", used in Asia

From the Change Date Format menu, you can select your preferred format, or just
press [ENTER] to leave the format unchanged.  If you select a format before
opening a data file, your selection will override the preferred format that was
saved with the data file.


  4b.  Changing the Time Format

From the Change Time Format menu, you can choose for times to be entered and
displayed with a 12-hour clock (with AM and PM) or a 24-hour clock (like
military time).  As with the date format, your selection here will override the
time format saved with a data file.


  4c.  Changing the Screen Width

When the Work Log program begins to run, the default printable area is 80
characters wide.  If you want the screen display to be wider or narrower, you
can change the maximum line width here, from a minimum of 40 characters to as
long as you would like.


  5.  Screen Header With Open File

When a file has been opened, the top of the screen will display:
    • The filename.  If the log has changed and the file has not been saved,
       "!NOT SAVED!" will also appear here.
    • The date and time that the file was last saved.  If the file has just been
       created and not been saved, "Never" will appear here.
    • The total number of entries (tasks) in the file.


  6.  Main Menu With Open File

Once a log file has been opened or created, the main menu changes to a list of
actions available for that file.  Those actions are:
    • [A] Add Entries
    • [F] Find/Edit/Delete Entries
    • [S] Save Log File
    • [C] Close Log File
    • [X] Change Settings

Entering [F] here will allow you to search for tasks based on various criteria.
You can then view, edit or delete tasks that match your search terms.


  7.  Help With Open File

When you are working with an open log file, before most prompts a brief help
screen will be displayed.  You can enter [-h] to turn this help text on or off.


  8.  Adding an Entry

After pressing [A] from the main menu, you will be guided through the steps of
adding a task to the log.  At each step, the top of the screen will show the
number of the entry being added, along with the items of information about the
task that you have entered so far.  As you go through the steps of adding a
task, you can at any point enter:
    • [-b] to go back to the previous item (except when adding a title, which is
       the first step)
    • [-q] to abort adding the entry (you will be asked to confirm your
       decision)


  8a.  Adding a Title

The title of a task can be any text string.  Tasks do not need to have unique
titles (and series of recurring tasks by default have identical titles).  Tasks
can include quotation marks and apostrophes, and wildcard characters like ? and
*, which can be searched for.  (See Appendix A for more on searching by text
string.)

  8b.  Adding a Date

The Work Log program allows you to enter dates in almost any way possible.  If
the year is omitted the date will default to the current year.  Date input can
include:
    • Numbers:  [3/10/2019], [3-10-19], [6.29.18]
    • Months and day spelled out:  [April 15, 2018], [Dec 25],
       [August twenty-third], [11 eighteenth] <-{November 18th}
    • Days relative to the current day:  [today], [yesterday], [tomorrow],
       [day after tomorrow]
       (NOTE:  Pressing [ENTER] will set the task to the current day.)
    • A day of the week:  [Thursday], [sun], [next Wed], [last Monday]
       (NOTE:  [last] denotes a day in the week preceeding the current week;
       [next] denotes a day in the week following.)

See Appendix B for a complete list of valid date entry formats, along with
notes and advisories.


  8c.  Adding a Starting Time

The Work Log program also allows a wide variety of input formats.  Time input
can include:
    • Numbers, in 12-hour or 24-hour time:  [12:30am], [1540], [11.15p]
       (NOTE:  Times between 12:00 and 11:59 will be assumed to be a.m.
        unless p.m. is indicated.)
    • Number words:  [three thirty-seven p.m.], [7 forty am], [noon], [midnight]
    • Relative times:  [15 till 6 pm], [twenty after 9 in the morning],
       [six 45 at night], [two fifteen in the afternoon]

See Appendix C for a complete list of valid time entry formats, along with notes
and advisories.


  8d.  Adding a Duration

To enter how long a task takes, you can either enter the amount of time
directly, or an ending time.  If you enter an ending time, the starting time
will be subtracted from it to determine the duration.  Durations can be entered
in days, hours and minutes.  (The program does not recognize seconds.)  Elements
of a duration do not need to be in order.  (The program will recognize both
[1 hour, 45 minutes] and [45m 1h] as a duration of an hour and 45 minutes.)  As
with dates and times, numbers may be entered as numerals or words.  Any carry-
overs will be converted (i.e., [ninety-five min] will be recognized as an hour
and 30 minutes).  See Appendix D for a complete listing of valid duration entry
formats.
(NOTE:  zero minutes is a valid duration.)


  8e.  Adding a Note

A note can be any text.  Press [ENTER] to leave the task note blank.
(NOTE:  Because [-b], [-h] and [-q] are reserved responses, a task note cannot
be any of these exact strings.  If you need to enter any of these strings as a
task note, add a blank space to the end.)


  8f.  Recurrance

You can decide here if you want to task to occur only one time, or recur at a
regular interval until a specific ending date is reached.  If you enter [no]
here, the task entry will be added to the log and you will be asked if you want
to add another task.  (If you answer [no] you will return to the main menu;
otherwise you will be taken to the start of another task entry.)


  9.  Setting a Task Recurrance

The Work Log program allows you to create a task, and then set it to recur at a
specified interval until a specified date.  For example, you can set a task
representing "Office Hours" for a Monday afternoon, and have it recur every
Monday (or every other Monday, or the 3rd Monday of every month, etc.) until a
date that you set.  The original task is the "parent" task, and the recurrances
are "child" tasks.  These tasks will all share a title, start time, duration,
and note; only the dates will be different.  (However, all of those items for
each child entry can be edited individually after they are added.)  Because task
recurrances are extremely flexible, you will be guided through a series of menus
to correctly set the recurrance interval.  At each step, you can choose to
go back, aborting the recurrance-setting and adding the task without any
recurrances.


  9a.  Choosing a Regular or Irregular Recurrance Interval

There are three types of regular recurrance intervals:  daily, weekly and
monthly.  If you select one of the regular intervals, you will be asked to enter
an end date, which must be after the date of the original task.  You can press
[ENTER] here to abort recurrance setting and add the task without recurrances.
For ALL other types of recurrance, including variations of the regular
recurrance intervals, select [OTHER].


  9b.  Choosing a Recurrance Interval Type

Irregular recurrance intervals fall into two broad categories:
    • Days of the week
    • Days of the month

This refers to the frame of reference for the interval pattern.  If the interval
is based on one or more days of the week, without regard to when during the
month those days are (such as every other Tuesday, or every fourth Friday), the
pattern is weekday-based.  If the pattern is based on specific days during EACH
month (either dates, such as the 3rd, the 15th, or the last day of the month; or
days, such as the 2nd Saturday or the 1st and 3rd Thursdays of the month), then
the pattern is month-based.  Be sure to examine your intended recurrance pattern
and make the correct choice here.


  9c-1.  Choosing the Day(s) of Recurrance

If you select a weekday-based pattern, you will be prompted to enter the day or
days on which you want the task to recur.  (NOTE:  these days do NOT need to
include the day on which the original task occurs.)  You can go back to select a
different recurrance pattern if you want.


  9c-2.  Choosing the Frequency of Recurrance

Once you have selected the day(s) on which you want the task to recur, you will
be asked if you want the task to recur every week, or less often.  Here you can
choose for the task to recur every week, every other week, every third week, or
less often.  If you select less often, you will be asked to enter the number of
weeks (up to 30) to skip between occurances.
(NOTE:  If you have chosen for your task to recur on more than one day of the
week, the number of weeks skipped between occurances must be the same for each
weekday.  For example, you cannot have a task recur every other Tuesday, but
every third Thursday.)


  9d-1.  Choosing Recurrance on Dates or Days During the Month

If you select a month-based pattern, you will first be asked to select whether
your recurrance pattern will be based on dates during the month (such as the
5th, 15th, or last day) or on days during the month (such as the third Tuesday
or the first and fourth Fridays) .  Make the choice that fits your recurrance
pattern.


  9d-2a.  Choosing the Recurrance Dates

If you select dates during the month, you will be prompted to enter the specific
dates during each month on which the task will recur.  These can be integers or
ordinals and can be numerals or spelled out [5, 16], [third, 24th].  To enter a
date relative to the end of the month, use negative numbers, with -1
representing the last day of the month, -2 the next to the last day, and so on
[15th, -1], [6, fifth to the last day].


  9d-2b1.  Choosing the Recurrance Days

If you select days during the month, you will be prompted to enter the day(s)
during the week that you want the task to recur.
(NOTE:  These days do NOT need to include the weekday on which the original task
occurs.)


  9d-2b2.  Choosing the Weeks in Each Month for Recurrance

Once you have selected the day(s) of the week on which you want the task to
recur, you will be prompted to enter on which week(s) during each month you want
the task to recur:
    • The first {day(s)}
    • The second {day(s)}
    • The third {day(s)}
    • The fourth {day(s)}
    • The fifth {day(s)}

(NOTE:  Because months do not have five full weeks, if you select the fifth
occurrance of a weekday, in any month that does not have a fifth occurrance of
that weekday, that recurrance will be skipped.)


  9e.  Entering an End Date

After you have set the recurrance interval for your task, you will be prompted
to enter the date after which recurrances will end.  This date can be entered in
the same fashion as any other date input.  If you do not enter a valid end date,
you will be prompted to re-enter the date.


  9f.  Confirming Recurrance Dates

Once you have entered an ending date, the program will display all of the dates
on which your task will recur, and ask if you want to proceed with adding those
tasks to the log.  If you respond [no], you will be asked to confirm your
decision, and if you do, the recurrances will be cancelled and the original task
will be added to the log without any recurrances.  If you confirm the recurrance
dates, the original task and all of the recurrances will be added to the log.


  10.  Searching for Entries

The Work Log program allows you to search for existing entries using four
distinct methods:
    • By Date/Time
    • By Duration
    • By Text Search
    • By RE Pattern

Begin your search by selecting the search method you would like to use.


  10a.  Searching by Date/Time

If you choose to search by date/time, you will be presented with a menu of three
kinds of date/time search:
    • A single date/time
    • A range of dates/times
    • View all dates

Select the kind of search you would like to perform.


  10a-1.  Searching by a Single Date/Time

If you select a single date/time, you will be prompted first to enter a date,
and then to enter a time.  If you want to search an entire day regardless of the
time, you can press [ENTER] at the time prompt to not enter a time.


  10a-2.  Searching by a Range of Dates/Times

If you choose to search a range of dates/times, you will be asked to first enter
a starting date and time, and then an ending date and time.  If you want to
search the entire day, you can press [ENTER] when prompted for a time.


  10a-3.  Viewing All Dates

Selecting this option will result in a display of all dates which contain
entries.


  10b.  Searching by Duration

If you choose to search by duration, you will be presented with the following
choices:
    • A specific duration
    • A range of durations

Select the scope of your search here.  If you choose to search for one specific
duration, you will be prompted to enter it.  You can enter an absolute duration
in any format available for duration entry.

If you choose to search for a range of durations, you will be asked to enter a
minimum and a maximum duration.  All searches will include the minimum and
maximum durations specified.  To search for all durations up to a certain limit,
enter [0 minutes] as the minimum duration.  To search for all durations above a
certain limit, enter [max] for the maximum duration.


  10c.  Searching by Text String

If you select to search by text, you will first be asked which field(s) you
would like to search:
    • Title
    • Notes
    • Title and Notes

After selecting the field(s) you would like to search, you will be prompted to
enter a string containing one or more search terms.  See Appendix A for a
comprehensive explanation of the Work Log program's search capabilities.


  10c-1.  Choosing Literal or Wildcard Search

If the text string you entered contains one or more of the wildcard characters
[?] or [*], you will be asked whether the program should treat those characters
as literal (meaning they will only match themselves) or as wildcards (where the
question mark will match any single character, and the asterisk will match any
number of characters).  You must choose one behavior or the other for all of the
question marks and asterisks in your text string.

If your text string does not contain any wildcard characters, this menu will not
appear.


  10d. Searching by RE Pattern

If you select this option, you will be asked to enter a string that is a valid
regular expression.  Do NOT use quotation marks when entering your expression.
All RE searches are CASE-SENSITIVE, UNLESS you append [, re.I] to the end of
your expression.  The program will attempt to compile the expression that you
enter, but otherwise will not try to validate it.


  11a.  Viewing All Results by Date

If you choose to view all entries by date, you will be shown a menu of dates
which contain log entries.  The menu will contain a maximum of nine dates; if
there are more than nine dates in total, the menu will include an option to move
to the next set of dates.  You can "page" back and forth between menu segments.
Selecting a date will allow you to browse all of the entries that fall on that
date.


  11b.  Viewing Matching Results

If you choose to search on specified criteria, the program will tell you how
many matches were found, and give you two options:
    • Browse all matching tasks
    • Choose from a list of matching tasks

Choose the option that you prefer.


  12.  Browsing Entries

When browsing entries, you will usually have five options:
    • [P] Previous
    • [N] Next
    • [E] Edit
    • [D] Delete
    • [B] Back

If you are viewing the first, last or only entry, the previous and/or next
options will not appear.  You can edit or delete the entry that you are
currently viewing.


  13.  Editing an Entry

The following fields of an entry can be edited:
    • Title
    • Date
    • Time
    • Duration
    • Notes

Fields are edited one at a time; you will be asked which field you want to edit.
Once you select a field, you can enter a new value for that field, or just press
[ENTER] to leave the original value unchanged.  Each time you make a change, the
entry will again be displayed, showing both the original values and changed
values for each field.  No changes will be made to the entry until you are
finished editing.  When you are finished editing, select [0] to go back.  You will then be asked if you want to save your changes.
(NOTE:  This will save your changes in memory, not to the data file.  To save
your changes permanently, you must save the data file from the main menu.)


  13a.  Making Changes to a Series of Entries

If the entry you are editing is part of a recurring series of tasks, you will be
asked if you want to apply your changes to all of the entries in the series.  If
you choose to apply your changes to the entire series, any previous changes made
to individual entries in the series will be overwritten.  If you choose to apply
your changes to only the current entry, the other entries in the series will be
unaffected.
(NOTE:  If you change the date of the current entry, you will NOT be asked if
you want to apply your changes to the series, even if you have also made edits
to other fields.)


  14.  Deleting an Entry or a Series of Entries

If you choose to delete an entry, and the entry is part of a recurring series of
tasks, you will be asked if you want to delete the entire series.  If you choose
not to delete the entire series, only the current task will be deleted.


  15.  Saving a File

Select [S] from the main menu to save the log file.  The program will inform you
that the file has been saved, and return you to the main menu to continue
working with the file.  If a problem occurs while saving the file, the program
will inform you of it.


  16.  Closing a File

Select [C] from the main menu to close the log file.  If the log has changed,
you will be asked whether or not you want to save the file.  After the file has
been closed, you will be returned to the initial main menu, where you can open
or create another file.


  17.  Quitting the Program

Select [Q] from the main menu to quit the program.  If the log has changed, you
will be asked if you want to save the file before exiting.


  Appendix A.  Text Searching

The Work Log program's search function operates similiarly to search functions
in other programs.  You can build a search using one or more terms, controlling
whether to include all the terms {AND}, any of the terms {OR}, or a combination.

(NOTE:  ALL searches are always case-insensitive.)

Each word you enter is a separate search term.  Words are only separated by
spaces--any hyphens or other punctuation marks attached to the word will be
included with the word.  [Twenty-three], [Morning!] and [questions???] are all
single search terms.  To make a single search term from multiple words, enclose
them in quotation marks.  ["Hello World!"] is a single search term.

All searches are {OR} searches unless specified otherwise.  This means that if
you enter more than one search term, the program will find any entry that matches any of those terms.  [study greek] will match any entry that contains
the word "study" AND any entry that contains the word "greek".

To perform an {AND} search, use the word "and" or the plus sign between two
terms.  [study and greek] or [study + greek] will match any entry that contains
BOTH the words "study" and "greek" (but not necessarily together).
(NOTE:  The {AND} operator and quotation marks do NOT produce the same results.
["study greek"] will only match that phrase, while [study + greek] will also
match entries like "Study my Greek homework" or "Greek Week - can't study".)

You do not need to specify an {OR} search, but you can use the word "or" or the
pipe symbol to indicate an {OR} search.  [study greek], [study or greek], and
[study | greek] will all produce identical results.

You can use parentheses to build complex searches utilizing both {AND} and {OR}.
Grouping search terms inside parentheses creates "superterms" which are
evaluated as a single unit.  [(study greek) + afternoon] will match entries that
contain either the word "study" OR the word "greek", but only if they ALSO
contain the word "afternoon".  You can nest parentheses to as many levels as you
want.

(EXAMPLE:  Searching for [Leslie and (lunch + date | (Alberto + dinner)) break]
will match any entry that:
    • contains the word "Leslie" AND--
        • the word "lunch" AND--
        • EITHER the word "date" OR--
        • BOTH the words "Alberto" AND "dinner"
    • OR contains the word "break"

In the absence of parentheses, search terms are evaluted left to right, with
neither {AND} nor {OR} taking precedence.)


  Appendix B.  Date Entry Formats

Dates can be entered in many ways.  For all of the general patterns listed
below, the positions of the day, month and year can be switched to follow any
date convention.

Numerals, separated by slashes, dashes or dots, with 2 or 4 digit years:
    • [3/15/19], [11-26-2017], [1.18.05]

(NOTE:  In the kinds of phrases listed below, you do not need to include
extraneous words like "the" and "of".  These words are ignored by the program.)

With month or day words, or with ordinals (abbrevated or not):
    • [June 15, 2019], [Apr 8th, 17], [December twenty-fifth]

The following words and phrases are valid, relative to the current day:
    • [today], [yesterday], [tomorrow], [day after yesterday],
       [day after tomorrow]

(WARNING!  The "current day" is dependent on the time and date according to the
server on which the program is running.  If you are running the program from a
remote server operating in another time zone, you may encounter unexpected
results.)

A day of the week, indicating that day during the current week, abbreviated or
not:
    • [Tuesday], [Fri], [Mo]

(WARNING!  A day of the week alone denotes that day of the current week, even if
that day is BEFORE the current day.  This is different from common English
usage, where naming a day by itself typically means the NEXT occurrance of that
day, even if happens during the next week.  For example, if you operate the
program on a Friday and enter [Monday] as a date, the program will interpret
that as the Monday four days earlier, not the Monday after the weekend.)

A day of the week as part of a phrase including [last], [next], [before last],
or [after next], which indicate that day of the week during the previous week,
the next week, two weeks previous, or two weeks in advance:
    • [next Tuesday], [last Fri], [the Monday before last], [Sat after next]

(WARNING!  The Work Log program operates on a standard calendar week, starting
on Sunday and ending on Saturday.  This is different from most computer
applications, including the Python language, which consider the week to begin on
Monday.)


  Appendix C.  Time Entry Formats

Times can be entered in a variety of ways.  For all of the patterns listed
below, times which are unambiguous in a 24-hour format (from 13:00 to 23:59) do
not need to be qualified, while times from 12:00 to 11:59 are generally assumed
to be AM, unless PM is specified.

(NOTE:  In all of the patterns below, AM or PM can be appended to the end of
the time in uppercase or lowercase letters, with or without periods, with or
without the "m", and with or without a space before a numeral.  You can also use
the words "morning", "afternoon", "evening" and "night" to indicate AM or PM.
You can include the words "in the" or "at", but they are ignored by the
program.)

Numerals, with or without a colon or dot:
    • [5am], [15:40], [330 p.m.], [2.15p], [8 in the morning]

For even hours, you can include the word "o'clock", though it is not necesary:
    • [6 o'clock a.m.], [11 o'clock at night]

Number words spelled out:
    • [eleven twenty-seven a.m.], [sixteen hundred], [two in the afternoon]

Time specific words:
    • [midnight], [noon]

Minutes before or after the hour, including the word "half":
    • [15 til 6 p.m.], [twenty after 9 in the morning], [5 before 10am],
       [13 until noon], [half 11 pm], [half past 3 in the morning]


  Appendix D.  Duration Entry Formats

The units for durations are "days", "hours" and "minutes".  These can be
abbreviated, and can follow a numeral without a space.  Number/unit combinations
can, but do not need to be, separated by commas.  Number words can be used.
    • [30 minutes], [1h], [3 hours 45 min], [0m], [eighty minutes]

(NOTE:  Because it is always possible to enter an ending time for a duration,
formats that mimic time formats (like "1:30" for an hour and 30 minutes) are not
allowed.)


{SCROLL UP TO VIEW THE MANUAL.}
{When you are finished, press [ENTER] to return to the program.}
"""
