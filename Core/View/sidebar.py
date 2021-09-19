# import tkinter gui modules
import tkinter as tk
from tkinter import ttk

# application console and powershell event logging
from datetime import datetime
from Model.util import log_message

# send new loading state to controller
from Model.util import loading_flag


class Sidebar(tk.Frame):
    """sidebar class"""

    def __init__(self, parent):
        tk.Frame.__init__(self, width=50, height=150, bg="blue")  # height=150
        self.parent = parent
        self.tree = None
        self.console = None
        self.body()

    def body(self):
        """defines gui elements in the sidebar gui section and their function calls"""

        # * profile tree overview
        # changed height from 25 to 27
        self.tree = ttk.Treeview(self, selectmode="browse", height=27)

        # * only console event log
        # added height=35 and changed width from 30 to 35
        self.console = tk.Text(self, height=35, width=35)
        self.console.config(state=tk.DISABLED)

        # * pack gui Items
        self.tree.pack(fill="both", expand=True)
        self.console.pack(side=tk.BOTTOM, fill="x")

    def load_profile(self):
        """handles profile loading of a selected webbrowser profile in the treeview"""
        selected = self.tree.focus()
        parent = self.tree.parent(selected)
        if self.tree.item(selected)["text"] in ["Firefox", "Chrome", "Edge"]:
            self.parent.controller.logger.warning("Bitte Profil auswählen!")
            return
        if selected and parent and self.tree.item(selected):
            browser = self.tree.item(parent)["text"]
            profile_name = self.tree.item(selected)["text"]
            # added status message for loading process
            log_message("Ladevorgang begonnen!", "info")
            loading_flag("True")  # , "ProgressBar START")
            time1 = datetime.now().strftime("um %H:%M:%S Uhr am %d.%m.%y: ")
            print(
                f' Start {time1} Profilladevorgang fuer Browserprofil:  "{profile_name}"  des Webbrowsers:  "{browser}"'
            )
            data = self.parent.controller.load_profile(
                browser, profile_name
            )  # start loading
            if data and data != "keep":
                # changed fillHistroyData to fillHistoryData !
                self.parent.content.fillHistoryData(data)
                # added status message for loading process
                log_message("Ladevorgang abgeschlossen!", "info")
                loading_flag("False")  # , "ProgressBar STOP")
                time2 = datetime.now().strftime("um %H:%M:%S Uhr am %d.%m.%y: ")
                print(
                    f'  Ende {time2} Profilladevorgang fuer Browserprofil:  "{profile_name}"  des Webbrowsers:  "{browser}"'
                )
            elif data and data == "keep":
                # added status message for loading process
                log_message("Ladevorgang abgebrochen!", "info")
                loading_flag("False")  # , "ProgressBar STOP")
                time2 = datetime.now().strftime("um %H:%M:%S Uhr: ")
                print(
                    f'    Abgebrochen {time2}    Profilladevorgang fuer Browserprofil:  "{profile_name}"  des Webbrowsers:  "{browser}"'
                )
                return
            else:
                # changed fillHistroyData to fillHistoryData !
                self.parent.content.fillHistoryData("None")

    def insert_profiles_to_treeview(self):
        """start search for new webbrowser profiles in default browser locations"""

        # * delete all profiles which have been found in previous searches
        for child in self.tree.get_children():
            self.tree.delete(child)

        log_message("Webrowser-Profile aktualisiert!", "info")
        profiles = self.parent.controller.load_profiles()  # refresh profile overview
        if profiles:
            for browser in profiles:
                parent = self.tree.insert("", "end", text=browser)
                for profile in profiles[browser]:
                    # ! filter out the deprecated empty firefox "default" profile for default-release channel firefox builds newer than v67
                    # * for firefox version previous to version 67
                    # * or other release channels - please deactivate filter)

                    # self.tree.insert(parent, "end", text=profile)

                    # * if you want to deactivate the filter comment out the if-loop below
                    # * and uncomment the function call above

                    if "default-release" in profile:
                        self.tree.insert(parent, "end", text=profile)
                    elif "Profil" in profile:
                        self.tree.insert(parent, "end", text=profile)
        else:
            log_message("Keine Profile gefunden!", "error")
            pass
