# import tkinter gui modules
import tkinter as tk
import os
from tkinter import ttk
from PIL import Image, ImageTk  # use images in tkinter module

# import dialog function from View.Dialogs.ask_dialog
from View.Dialogs.ask_dialog import AskDialog  # confirmation popup window

# import utility functions from Model.util
from Model.util import resource_path  # get absolute path to temp _MEIPASS location
from Model.util import (
    log_message,
)  # sends log message to log listener in controller module


class Toolbar(tk.Frame):
    """toolbar class"""

    def __init__(self, parent):
        tk.Frame.__init__(self, bd=1, relief=tk.RAISED)
        self.parent = parent
        self.progressBar = None
        self.body()

    def body(self):
        """defines gui elements in the toolbar gui section and their function calls"""

        # * buttons - icon setup
        img_first = Image.open(resource_path("Core\\View\\icons\\Exit_Icon.png"))
        exit_img = ImageTk.PhotoImage(img_first)
        exit_img = exit_img._PhotoImage__photo.subsample(15)

        img_sec = Image.open(resource_path("Core\\View\\icons\\Rollback_Icon.png"))
        rollback_img = ImageTk.PhotoImage(img_sec)
        rollback_img = rollback_img._PhotoImage__photo.subsample(15)

        img_third = Image.open(resource_path("Core\\View\\icons\\Save_Icon.png"))
        save_img = ImageTk.PhotoImage(img_third)
        save_img = save_img._PhotoImage__photo.subsample(15)

        img_fourth = Image.open(resource_path("Core\\View\\icons\\Reload_Icon.png"))
        reload_img = ImageTk.PhotoImage(img_fourth)
        reload_img = reload_img._PhotoImage__photo.subsample(15)

        img_fifth = Image.open(resource_path("Core\\View\\icons\\Load_Icon.png"))
        load_img = ImageTk.PhotoImage(img_fifth)
        load_img = load_img._PhotoImage__photo.subsample(15)

        # * save profile changes button configuration
        # changed safeButton to saveButton
        saveButton = tk.Button(
            self,
            image=save_img,
            relief=tk.FLAT,
            command=self.parent.controller.commit_all_data,
        )
        saveButton.image = save_img

        # * refresh profile tree view button configuration
        profileButton = tk.Button(
            self,
            image=reload_img,
            relief=tk.FLAT,
            command=self.parent.sidebar.insert_profiles_to_treeview,
        )
        profileButton.image = reload_img

        # * exit application button configuration
        exitButton = tk.Button(
            self, image=exit_img, relief=tk.FLAT, command=self.on_quit
        )
        exitButton.image = exit_img

        # * activity indicator configuration
        self.progressBar = ttk.Progressbar(
            self, orient="horizontal", length=130, maximum=30, mode="determinate"
        )

        # * load profile button configuration
        loadButton = tk.Button(
            self,
            image=load_img,
            relief=tk.FLAT,
            command=self.parent.sidebar.load_profile,
        )
        loadButton.image = load_img

        # * rollback button configuration
        rollbackButton = tk.Button(
            self,
            image=rollback_img,
            relief=tk.FLAT,
            command=self.parent.controller.rollback_all_data,
        )
        rollbackButton.image = rollback_img

        # * pack gui elements - determines postitions in relation to each other
        saveButton.pack(side=tk.LEFT, padx=4, pady=2)
        profileButton.pack(side=tk.LEFT, padx=4, pady=2)
        exitButton.pack(side=tk.LEFT, padx=4, pady=2)
        self.progressBar.pack(side=tk.LEFT, padx=4, pady=1)
        loadButton.pack(side=tk.LEFT, padx=4, pady=2)
        rollbackButton.pack(side=tk.LEFT, padx=4, pady=2)

    def monitor_activity(self, flag):
        """updates the gui module - progessbar - as activity indicator for the profile loading"""
        if flag == "True":
            self.progressBar["value"] = 100  # Progressbar full green
        elif flag == "False":
            self.progressBar["value"] = 0  # Progressbar empty grey
        else:
            # log_message("Unbekannter Status des Ladevorgangs erkannt", "error")
            pass

    def on_quit(self):
        """ask for confirmation if application should be closed and delete advanced.log file on_quit click"""

        log_message("Fehlerspeicher wird gelöscht\n          - Fortfahren ? -", "warning")

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
