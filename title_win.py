import pywinctl as pwc
import time
import re

title_left = '<DeaDBeeF> '
title_right = ' </DeaDBeeF>'
title_match = f'{title_left}(.*?){title_right}'  # do not strip title_left or title_right here


def _changedTitleCB(title: str):
    print("NEW title", title)


def set_title_change_polling(callback=_changedTitleCB, match=title_match):
    last_title = None
    while True:
        try:
            for title in pwc.getAllTitles():
                if re.match(match, title):
                    if title != last_title:
                        last_title = title
                        callback(title)
        except KeyboardInterrupt:
            break
        time.sleep(0.1)


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

if __name__ == '__main__':
    set_title_change_polling()
