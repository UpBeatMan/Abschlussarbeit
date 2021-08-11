import tkinter as tk
from tkinter.constants import HORIZONTAL
from PIL import Image, ImageTk  #
from View.Dialogs.ask_dialog import AskDialog  # confirmation popup window
from Model.util import resource_path  # get absolute path to temp _MEIPASS location

# from tkinter.ttk import Progressbar, Style
from tkinter import ttk
from time import sleep
from tkinter import Label


class Toolbar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, bd=1, relief=tk.RAISED)
        self.parent = parent

        self.progressBar = None
        # * where should I put my flag to start this activity progress bar indicator
        # ! self.load_activity_flag = None

        self.body()

    def body(self):

        img_first = Image.open(resource_path("Core/View/icons/Exit_Icon.png"))
        exit_img = ImageTk.PhotoImage(img_first)
        exit_img = exit_img._PhotoImage__photo.subsample(15)

        img_sec = Image.open(resource_path("Core/View/icons/Rollback_Icon.png"))
        rollback_img = ImageTk.PhotoImage(img_sec)
        rollback_img = rollback_img._PhotoImage__photo.subsample(15)

        img_third = Image.open(resource_path("Core/View/icons/Save_Icon.png"))
        save_img = ImageTk.PhotoImage(img_third)
        save_img = save_img._PhotoImage__photo.subsample(15)

        img_fourth = Image.open(resource_path("Core/View/icons/Reload_Icon.png"))
        reload_img = ImageTk.PhotoImage(img_fourth)
        reload_img = reload_img._PhotoImage__photo.subsample(15)

        img_fifth = Image.open(resource_path("Core/View/icons/Load_Icon.png"))
        load_img = ImageTk.PhotoImage(img_fifth)
        load_img = load_img._PhotoImage__photo.subsample(15)

        # * changed safeButton to saveButton
        saveButton = tk.Button(
            self,
            image=save_img,
            relief=tk.FLAT,
            command=self.parent.controller.commit_all_data,
        )
        saveButton.image = save_img

        exitButton = tk.Button(self, image=exit_img, relief=tk.FLAT, command=self.quit)
        exitButton.image = exit_img

        profileButton = tk.Button(
            self,
            image=reload_img,
            # text="Profile aktualisieren",
            relief=tk.FLAT,
            command=self.parent.sidebar.insert_profiles_to_treeview,
        )
        profileButton.image = reload_img

        loadButton = tk.Button(
            self,
            image=load_img,
            relief=tk.FLAT,
            command=self.parent.sidebar.load_profile,
        )
        loadButton.image = load_img

        rollbackButton = tk.Button(
            self,
            image=rollback_img,
            relief=tk.FLAT,
            command=self.parent.controller.rollback_all_data,
        )
        rollbackButton.image = rollback_img

        # # progressbar theme:
        # theme = ttk.Style()
        # theme.theme_use("winnative")
        # theme.configure("green.Horizontal.TProgressbar", background="green")

        # # progressbar:
        # self.bar = ttk.Progressbar(
        #     self.parent,
        #     style="green.Horizontal.TProgressbar",
        #     orient="horizontal",
        #     mode="indeterminate",
        #     length="180",
        # )

        # # update root to see animation:
        # self.parent.update()
        # self.play_animation()

        loading = Label(self, text="Daten werden geladen...", fg="green")

        self.progressBar = ttk.Progressbar(
            self, orient=HORIZONTAL, length=160, mode="determinate"
        )

        saveButton.pack(side=tk.LEFT, padx=4, pady=2)
        profileButton.pack(side=tk.LEFT, padx=4, pady=2)
        exitButton.pack(side=tk.LEFT, padx=4, pady=2)
        loading.pack(side=tk.LEFT, padx=4, pady=2)
        self.progressBar.pack(side=tk.LEFT, padx=4, pady=1)
        loadButton.pack(side=tk.LEFT, padx=4, pady=2)

        rollbackButton.pack(side=tk.LEFT, padx=4, pady=2)

        # self.start()

        # while True:
        #     status = self.get_load_activity_flag()
        #     if status == True:
        #         self.start()
        #     elif status == False:
        #         self.stop()
        #     else:
        #         pass  # error: no valid flag state

    # originally in Config/__init__.pz
    # def set_load_activity_flag(self, switch: bool):
    #     self.load_activity_flag = switch

    # def get_load_activity_flag(self):
    #     status =  self.load_activity_flag
    #     return status

    def start(self):
        self.progressBar.start()

    def stop(self):
        self.progressBar.stop()

    # progressbar animation:
    # def play_animation(self):
    #     for i in range(2000):
    #         self.bar["value"] += 1
    #         self.parent.update_idletasks()
    #         sleep(0.01)
    #     else:
    #         self.root.destroy()
    #         exit(0)

    def quit(self):
        if self.parent.controller.get_unsaved_handlers():
            answer = AskDialog(
                self.parent,
                self.parent.controller,
                "Es wurden nicht alle Daten gespeichert!\n Trotzdem fortfahren?",
            ).show()
            if not answer:
                return
        answer = AskDialog(
            self.parent, self.parent.controller, "Möchten Sie wirklich beenden?"
        ).show()
        if not answer:
            return
        self.parent.destroy()
