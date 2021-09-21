 # ToolKit module
import tkinter as tk
# get absolute path to temp _MEIPASS location
from Model.util import resource_path


class GuideDialog(tk.Toplevel):
    """GuideDialog class opens a popup window"""

    # * toplevel popup window - display brief application guide
    # * a windows with text content and an okay button to close it again

    def __init__(self, parent, controller):
        """run __init__ section at class instantiation"""

        # * create a reference to parent window
        tk.Toplevel.__init__(self, parent)
        # * set window title
        self.title("Nutzerhandbuch")
        # * lock window size
        self.resizable(0, 0)

        self.controller = controller

        self.text_frame = tk.Frame(self, width=130)  # a frame to organize other widgets
        self.text = tk.Text(self.text_frame, width=130)  # a text field widget
        self.text.config(state=tk.DISABLED)  # disabled text widget
        # organizes widget in blocks before placing them in the parent widget
        self.text.pack()
        self.text_frame.pack(side=tk.TOP)
        # import text from Core/View/text/guide.txt
        self.file_to_text()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(
            button_frame, text="Ok", width=15, command=self.on_ok
        )

        self.ok_button.pack()

    def file_to_text(self):
        """read text from guide.txt and insert it to the text widget"""
        text = u""
        self.text.config(state=tk.NORMAL)
        guide = open(resource_path("Core\\View\\text\\guide.txt"), "r")
        for line in guide.readlines():
            text += line
        self.text.insert(tk.INSERT, text)
        self.text.config(state=tk.DISABLED)

    def on_ok(self, event=None):
        """closes window on_ok click"""
        self.destroy()

    def show(self):
        """shows a hidden tk widget again"""
        # * displays the window, after using either the iconify or the withdraw methods
        self.wm_deiconify()
        # * this method can be called after the event which needs to happen before the window event
