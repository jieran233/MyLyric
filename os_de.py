import sys
import os

os_de = {'windows': 'win32', 'linux_gnome': 'gnome'}


def get_os_de():
    """
    Get operating system platform, and desktop environment for linux.
    """

    platform = sys.platform
    if platform.startswith('win32'):
        return os_de['windows']

    elif platform.startswith('linux'):
        # https://stackoverflow.com/a/2035664
        desktop = os.environ.get('DESKTOP_SESSION')
        if desktop:  # Not None
            if desktop.startswith('gnome'):
                return os_de['linux_gnome']
            else:
                raise Exception("Unsupported desktop environment (only gnome is supported)")
    else:
        raise Exception("Unsupported platform (only win32 and linux are supported)")
