import subprocess
import ast
import time

title_left = '<DeaDBeeF> '
title_right = ' </DeaDBeeF>'
suffix_default = title_right
functions = {'title': 'getWindowsByTitle',
             'prefix': 'getWindowsByPrefix',
             'suffix': 'getWindowsBySuffix',
             'substring': 'getWindowsBySubstring'}

command = ("gdbus call --session --dest org.gnome.Shell --object-path /io/github/jieran233/GetAllTitlesOfWindows "
           "--method io.github.jieran233.GetAllTitlesOfWindows.{} '{}'").format(functions['suffix'], suffix_default)

output_left = ['(', '(@as']
output_right = ',)'


def _changedTitleCB(_title: str):  # Callback function for handling title changes
    print("NEW title", _title)  # Printing the new title


def set_title_change_polling(callback=_changedTitleCB, _command=command):
    last_title = None
    while True:
        try:
            # Use subprocess.Popen to start the system command and capture its output through stdout=subprocess.PIPE
            process = subprocess.Popen(_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                # Read command output
                output = process.stdout.readline()
                if not output:
                    break
                output = output.decode().strip()  # Remove newlines from output and print
                # print(output)
                for lstrip in output_left:
                    output = output.lstrip(lstrip)
                output = output.rstrip(output_right)
                output = output.strip()

                titles_list = ast.literal_eval(output)

                if titles_list:  # Check if the list is not blank
                    title = titles_list[0]
                    if title != last_title:
                        last_title = title
                        callback(title)

            # Wait for the command to complete
            process.wait()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("title_gnome Error:", e)
            raise e
        time.sleep(0.1)


if __name__ == '__main__':
    set_title_change_polling()
