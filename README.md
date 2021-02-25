# Wikipedia Data Stream Handling

__Wikipedia Watching__

wiki.py is the code which prints Domain and User reports on changes made in Wikipedia domains. The following are the reports generated: 
1. **Domain report**:
  Prints the number of the Wikipedia domains that have been updated, followed by a list of the domains sorted by the count of how many unique pages were updated on each. Pages with the same title are assumed to be the same.
2. **User report**:
  Prints a list of users that have made changes to en.wikipedia.org domain, sorted by their total edit count (available as performer->user_edit_count in each event). If the same user shows up multiple times in the given time period, then uses the highest edit count seen for them.
  
Each report is available in 1 minute format and 5 minute format with minute-wise reports.

__How to Run__

The code is a python file which has to be run via the terminal as:
> python wiki.py

_Requirements_
* Python 3 installed in the user device following which the code can be downloaded and run directly from the terminal/GUI.
* The code requires the user to give input regarding the report required. A menu with the same appears on stdout when the code is run.
* Following the input given by the user, the report for the same is generated.
* No libraries are required to be downloaded

By Navin Mundhra
