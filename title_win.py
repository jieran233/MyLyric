import pywinctl as pwc  # Importing the pywinctl module for Windows control operations
import time  # Importing the time module for sleep function
import re  # Importing the re module for regular expressions

match_default = r"<DeaDBeeF>(.*?)<\/DeaDBeeF>"  # Regular expression pattern for matching titles


def _changedTitleCB(title: str):  # Callback function for handling title changes
    print("NEW title", title)  # Printing the new title


def set_title_change_polling(callback=_changedTitleCB, match=match_default):
    """
    Function to continuously poll for title changes and execute a callback function.

    :param callback: Function to be called when a new title matching the pattern is found
    :param match: Regular expression pattern to match titles
    """
    last_title = None  # Initializing last_title variable
    while True:  # Infinite loop for continuous polling
        try:
            for title in pwc.getAllTitles():  # Iterating over all titles
                if re.match(match, title):  # Checking if the title matches the pattern
                    if title != last_title:  # Checking if the title has changed
                        last_title = title  # Updating last_title
                        callback(title)  # Calling the callback function with the new title
        except KeyboardInterrupt:  # Handling KeyboardInterrupt to exit the loop
            break  # Exiting the loop
        time.sleep(0.1)  # Sleeping for 0.1 seconds to avoid high CPU usage

# def set_title_change_callback(callback=_changedTitleCB, match=match_default):
#     matched_windows = pwc.getWindowsWithTitle(match, condition=pwc.Re.MATCH)
#     npw = matched_windows[0]
#     npw.watchdog.start(changedTitleCB=callback)
#     npw.watchdog.setTryToFind(True)
#     i = 0
#     while True:
#         try:
#             if i == 50:
#                 npw.watchdog.updateCallbacks(changedTitleCB=callback)
#             if i == 100:
#                 npw.watchdog.updateInterval(0.1)
#                 npw.watchdog.setTryToFind(False)
#             time.sleep(0.1)
#         except KeyboardInterrupt:
#             break
#         i += 1
#     npw.watchdog.stop()
