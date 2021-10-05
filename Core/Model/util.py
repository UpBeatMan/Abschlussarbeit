import os  # miscellaneous operating system interfaces
import sys  # system-specific parameters and functions
from datetime import datetime  # datetime object containing date and time
from pubsub import pub  #  publish module
import platform  # access to underlying platform's identifying data

if platform.system() == "Windows":
    # * importing an interface for the win32 File APIs
    from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
    from win32file import (
        GENERIC_WRITE,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        FILE_SHARE_WRITE,
    )


def log_message(message, lvl, debug="Keine Debugmeldung vorhanden"):
    """unifies sending process of log data to the logging listener in the controller module"""

    pub.sendMessage("logging", message=message, lvl=lvl, debug=debug)


def loading_flag(flag):
    """sets flag state and sends it to the activity listener in the controller module"""

    pub.sendMessage("activity", flag=flag)


def change_file_time(path, delta):
    if not os.path.exists(path):
        log_message(
            "Datei existiert nicht mehr",
            "debug",
            "Zeitinformationen der Datei: \n    "
            + path
            + " können nicht manipuliert werden. \n    Diese Datei existiert nicht mehr",
        )
        return
    if platform.system() == "Windows":
        # * modify filetimes on Windows
        fh = CreateFile(
            path,
            GENERIC_WRITE,
            FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            FILE_FLAG_BACKUP_SEMANTICS,
            0,
        )
        cTime, aTime, mTime = GetFileTime(fh)
        cTime = datetime.fromtimestamp(cTime.timestamp() - delta)
        aTime = datetime.fromtimestamp(aTime.timestamp() - delta)
        mTime = datetime.fromtimestamp(mTime.timestamp() - delta)
        SetFileTime(fh, cTime, aTime, mTime)
        CloseHandle(fh)
    else:
        # modify filetimes on Linux/Mac
        a_time = os.path.getatime(path)
        m_time = os.path.getmtime(path)
        a_time = a_time - delta
        m_time = m_time - delta
        os.utime(path, (a_time, m_time))
        # * add manual creation time workaround - open and work with the change_ctime.sh bash script in Core/Model/ directory
        # https://stackoverflow.com/questions/16126992/setting-changing-the-ctime-or-change-time-attribute-on-a-file/17066309#17066309


def resource_path(relative_path):
    """resource_path gets absolute path to resource,
    works for dev and for PyInstaller"""
    try:
        # * PyInstaller creates a temp folder
        # * and stores the absolute path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
