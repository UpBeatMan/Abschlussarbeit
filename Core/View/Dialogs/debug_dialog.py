# ToolKit module
import tkinter as tk

# get absolute path to temp _MEIPASS location
from Model.util import resource_path


class DebugDialog(tk.Toplevel):
    """DebugDialog class opens a popup window"""

    # * toplevel popup window - displays debug and error log

    def __init__(self, parent, controller):
        """run __init__ section at class instantiation"""

        # * create a reference to parent window
        tk.Toplevel.__init__(self, parent)
        # * set window title
        self.title("Debugmodus")
        # * lock window size
        self.resizable(0, 0)

        self.controller = controller

        # * a frame to organize other widgets
        self.text_frame = tk.Text(self, width=150)  # 160
        # * the debug and error log frame
        self.text = tk.Text(self.text_frame, width=150)  # 160
        self.text.config(state=tk.DISABLED)
        # * place(pack) text elements
        self.text.pack()
        self.text_frame.pack(side=tk.TOP)

        # * button area
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)
        # * button configuration
        self.ok_button = tk.Button(
            button_frame, text="Ok", width=15, command=self.on_ok
        )
        self.refresh_button = tk.Button(
            button_frame, text="Aktualisieren", width=15, command=self.on_refresh
        )

        # * place(pack) buttons in gui area
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)

        # * import saved log data (including every log level)
        # * from Core/advanced.log
        self.load_debuglog()

    def load_debuglog(self):
        """read text from advanced.log and insert it to the text widget"""

        # * create a unicode text string
        text = u""
        # * editing activated
        self.text.config(state=tk.NORMAL)
        # * open advanced.log
        guide = open(resource_path("Core\\advanced.log"), "r")
        # * add line by line to text variable
        for line in guide.readlines():
            text += line
        # * insert text variable to text field
        self.text.insert(tk.INSERT, text)
        # * editing disabled
        self.text.config(state=tk.DISABLED)

    def on_ok(self, event=None):
        """close windows when clicking ok"""
        self.destroy()

    def on_refresh(self, event=None):
        """clear text field and load advanced.log again"""
        # * editing activated
        self.text.config(state=tk.NORMAL)
        # * clear text field
        self.text.delete("1.0", "end")
        # * editing disabled
        self.text.config(state=tk.DISABLED)
        # * load advanced.log again
        self.load_debuglog()

    def show(self):
        """shows a hidden tk widget again"""
        # * displays the window, after using either the iconify or the withdraw methods
        self.wm_deiconify()
        # * this method can be called after the event which needs to happen before the window event
        self.wait_window()
