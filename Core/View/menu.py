# import tkinter gui modules
import tkinter as tk  # ToolKit module
import webbrowser  # webrowser module
import os

# import popup gui elements from View.Dialog.ask_dialog and *.guide_dialog
from View.Dialogs.ask_dialog import AskDialog  # confirmation window
from View.Dialogs.guide_dialog import GuideDialog  # manual txt viewer
from View.Dialogs.debug_dialog import DebugDialog  # debug mode

from Model.util import resource_path  # get absolute path to temp _MEIPASS location
from Model.util import (
    log_message,
)  # sends log message to log listener in controller module


class MainMenu(tk.Menu):
    """menu bar class"""

    def __init__(self, parent):
        tk.Menu.__init__(self)
        self.parent = parent  # parent tk widget
        # menu items
        self.filemenu = None
        self.editmenu = None
        self.viewmenu = None
        # body
        self.body()

    def body(self):
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(
            label="Alle Änderungen speichern",
            command=self.parent.controller.commit_all_data,  # * trigger commit for all changes
        )
        self.filemenu.add_command(label="Beenden", command=self.on_quit)
        self.add_cascade(label="Datei", menu=self.filemenu)

        self.editmenu = tk.Menu(self, tearoff=0)
        self.editmenu.add_command(
            label="Undo", command=self.parent.controller.rollback_all_data
        )
        self.editmenu.add_command(
            label="Alle Daten editieren", command=self.parent.controller.edit_all_data
        )
        self.editmenu.add_command(
            label="Ausgewählte Daten editieren",
            command=self.parent.controller.edit_selected_data,
        )
        self.editmenu.add_command(
            label="Dateisystem-Zeit anpassen",
            command=self.parent.controller.change_filesystem_time,
        )
        self.editmenu.add_command(
            label="Dateisystem-Zeit zurücksetzten",
            command=self.parent.controller.rollback_filesystem_time,
        )
        self.add_cascade(label="Bearbeiten", menu=self.editmenu)

        self.viewmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Ansicht", menu=self.viewmenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(
            label="Hilfe",
            command=lambda: GuideDialog(self.parent, self.parent.controller).show(),
        )
        helpmenu.add_command(
            label="Über...",
            command=lambda: webbrowser.open_new(
                "https://github.com/UpBeatMan/Abschlussarbeit"
            )
            # "https://github.com/hirthirt/fiprotima"
        )
        self.add_cascade(label="Hilfe", menu=helpmenu)

        debugmenu = tk.Menu(self, tearoff=0)
        debugmenu.add_command(
            label="Öffnen",
            command=lambda: DebugDialog(self.parent, self.parent.controller).show()
            # self.parent.controller.open_debugwin
        )
        self.add_cascade(label="Debugmodus", menu=debugmenu)

    def firefox_views(self):
        self.viewmenu.delete(0, "end")
        self.viewmenu.add_command(
            label="Historie",
            command=lambda: self.parent.controller.change_data_view("History"),
        )
        self.viewmenu.add_command(
            label="Cookies",
            command=lambda: self.parent.controller.change_data_view("Cookie"),
        )
        self.viewmenu.add_command(
            label="Favicons",
            command=lambda: self.parent.controller.change_data_view("Favicon"),
        )
        self.viewmenu.add_command(
            label="Downloads",
            command=lambda: self.parent.controller.change_data_view("Download"),
        )
        self.viewmenu.add_command(
            label="Logins",
            command=lambda: self.parent.controller.change_data_view("Login"),
        )
        self.viewmenu.add_command(
            label="Lesezeichen",
            command=lambda: self.parent.controller.change_data_view("Bookmarks"),
        )
        self.viewmenu.add_command(
            label="Cache",
            command=lambda: self.parent.controller.change_data_view("Cache"),
        )
        self.viewmenu.add_command(
            label="Profil",
            command=lambda: self.parent.controller.change_data_view("FireProfile"),
        )
        self.viewmenu.add_command(
            label="Addons",
            command=lambda: self.parent.controller.change_data_view("Addons"),
        )
        self.viewmenu.add_command(
            label="Formular-Historie",
            command=lambda: self.parent.controller.change_data_view("FormHistory"),
        )
        self.viewmenu.add_command(
            label="Extensions",
            command=lambda: self.parent.controller.change_data_view("Extensions"),
        )
        self.viewmenu.add_command(
            label="Session",
            command=lambda: self.parent.controller.change_data_view("Session"),
        )
        self.viewmenu.add_command(
            label="Berechtigungen",
            command=lambda: self.parent.controller.change_data_view("Permission"),
        )
        self.viewmenu.add_command(
            label="Website-Präferenzen",
            command=lambda: self.parent.controller.change_data_view("ContentPref"),
        )

    def chrome_edge_views(self):
        self.viewmenu.delete(0, "end")
        self.viewmenu.add_command(
            label="Historie",
            command=lambda: self.parent.controller.change_data_view("History"),
        )
        self.viewmenu.add_command(
            label="Cookies",
            command=lambda: self.parent.controller.change_data_view("Cookie"),
        )
        self.viewmenu.add_command(
            label="Favicons",
            command=lambda: self.parent.controller.change_data_view("Favicon"),
        )
        self.viewmenu.add_command(
            label="Downloads",
            command=lambda: self.parent.controller.change_data_view("Download"),
        )
        self.viewmenu.add_command(
            label="Logins",
            command=lambda: self.parent.controller.change_data_view("Login"),
        )
        self.viewmenu.add_command(
            label="Lesezeichen",
            command=lambda: self.parent.controller.change_data_view("Bookmarks"),
        )
        self.viewmenu.add_command(
            label="Cache",
            command=lambda: self.parent.controller.change_data_view("Cache"),
        )
        self.viewmenu.add_command(
            label="Profil",
            command=lambda: self.parent.controller.change_data_view("Profile"),
        )
        self.viewmenu.add_command(
            label="Keywords",
            command=lambda: self.parent.controller.change_data_view("Keywords"),
        )
        self.viewmenu.add_command(
            label="Formular-Eingaben",
            command=lambda: self.parent.controller.change_data_view("Autofill"),
        )
        self.viewmenu.add_command(
            label="Media",
            command=lambda: self.parent.controller.change_data_view("Media"),
        )
        self.viewmenu.add_command(
            label="Erweiterungs-Cookies",
            command=lambda: self.parent.controller.change_data_view("ExtCookies"),
        )
        self.viewmenu.add_command(
            label="Unsichere Anmeldedaten",
            command=lambda: self.parent.controller.change_data_view("CompCred"),
        )

    def on_quit(self):
        """ask for confirmation if application should be closed and delete advanced.log file on_quit click"""

        log_message(
            "Fehlerspeicher wird gelöscht\n          - Fortfahren ? -", "warning"
        )

        if self.parent.controller.get_unsaved_handlers():
            # notify that changes are not saved yet
            answer = AskDialog(
                self.parent,
                self.parent.controller,
                "Änderungen noch nicht gespeichert!\nTrotzdem beenden?",
            ).show()
            if not answer:
                return
        else:
            answer = AskDialog(
                self.parent,
                self.parent.controller,
                "Möchten Sie wirklich beenden?",
            ).show()
            if not answer:
                return

        # * delete advanced.log file
        log_message("close logging", "delete")
        advanced_log_path = resource_path("Core\\advanced.log")
        os.remove(advanced_log_path)

        # * exit tkinter application
        self.parent.destroy()
