# import tkinter gui modules
import tkinter as tk  # ToolKit module
import os  # delete advanced.log on_close click

# import view sub modules and gui sections menu, toolbar, sidebar and content
from View.menu import MainMenu
from View.toolbar import Toolbar
from View.sidebar import Sidebar
from View.content import Content

# import dialog functions from View.Dialogs.ask_dialog and ".DebugDialog
from View.Dialogs.ask_dialog import AskDialog  # confirmation popup window

# ! from View.Dialogs.debug_dialog import DebugDialog

# get absolute path to temp _MEIPASS location
from Model.util import resource_path

# sends log message to log listener in controller module
from Model.util import log_message


class View(tk.Tk):
    """View class is the root gui file and handles all gui elements"""

    def __init__(self, controller):
        """runs __init__ section at class instantiation"""

        super().__init__()
        # * sets initial size of application window
        self.geometry("1600x900")
        # * sets the application window title
        self.title("Digital Forensics Scenario Creator")
        # * sets the application icon
        icon = tk.PhotoImage(file=resource_path("Core\\View\\icons\\Logo_Icon.png"))
        self.iconphoto(False, icon)

        # * instantiate controller - The controller is the intermediary between View interaction elements and the Model backend of DFSC
        self.controller = controller
        # * instantiate main gui sections(submodules)
        self.menu = None
        self.toolbar = None
        self.sidebar = None
        self.content = None

        self.body()

    def main(self):
        """runs tkinter mainloop() and triggers pre-exit confirmation"""

        # * first call function on_close before closing the windows
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # * runs tkinter gui !
        self.mainloop()

        # info:
        # the loading indicator is a workaround, which is using a predicted gui freeze for its advantage.
        # explanation:
        # a resource conflict between load_profile and the mainloop causes the gui to freeze during the loading time.
        # reason:
        # tkinter is not designed for parallel high intensive function calls.
        # theory for a clean solution:
        # One solution could be outsourcing the whole gui in its own Thread with multithreading. Was too time consuming to solve now.
        # TBD in future developments. Also there is still an open question, if this approach is compatible with the MVC architecture!

    def body(self):
        """defines structure of different gui submodules towards each other"""

        # * instantiate gui section with self argument as parent(root tk window)
        self.content = Content(self)
        self.sidebar = Sidebar(self)
        self.menu = MainMenu(self)
        self.toolbar = Toolbar(self)

        # * defines gui structure
        self.config(menu=self.menu)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="nwes")
        self.sidebar.grid(row=1, column=0, sticky="nwes")
        self.content.grid(row=1, column=1, sticky="nwes")  # wens
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def on_close(self):
        """ask for confirmation if application should be closed and delete advanced.log file on_close click"""

        log_message(
            "Fehlerspeicher wird gelöscht\n          - Fortfahren ? -", "warning"
        )

        # * ask for confirmation to close application
        if self.controller.get_unsaved_handlers():
            # notify that changes are not saved yet
            answer = AskDialog(
                self,
                self.controller,
                "Änderungen noch nicht gespeichert!\nTrotzdem beenden?",
            ).show()
            if not answer:
                return
        else:
            answer = AskDialog(
                self,
                self.controller,
                "Möchten Sie wirklich beenden?",
            ).show()
            if not answer:
                return

        # * delete advanced.log file
        log_message("close logging", "delete")
        advanced_log_path = resource_path("Core\\advanced.log")
        os.remove(advanced_log_path)

        # * exit tkinter application
        self.destroy()
