import tkinter as tk  # ToolKit module
from Model.util import resource_path  # get absolute path to temp _MEIPASS location


class GuideDialog(tk.Toplevel):  # toplevel - popup confirmation window
    # * a windows with text and an okay button to close it again
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Nutzerhandbuch")
        self.resizable(0, 0)

        self.controller = controller

        self.text_frame = tk.Frame(self, width=130)  # a frame to organize other widgets
        self.text = tk.Text(self.text_frame, width=130)  # a text field widget
        self.text.config(state=tk.DISABLED)  # disabled text widget
        # organizes widget in blocks before placing them in the parent widget
        self.text.pack()
        self.text_frame.pack(side=tk.TOP)
        # import text from ./View/text/guide.txt
        self.file_to_text()

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(
            button_frame, text="OK", width=15, command=self.on_ok
        )

        self.ok_button.pack()  # organizes widgets in blocks before placing them in the parent widget

    def on_ok(self, event=None):
        self.destroy()  # destroy windows when clicking ok

    def show(self):
        # * show a hidden tk widget again
        self.wm_deiconify()  # displays the window, after using either the iconify or the withdraw methods
        self.wait_window()  # this method can be called after the event which needs to happen before the window event

    def file_to_text(self):
        # * read text from guide.txt and insert it to the text widget
        text = u""
        self.text.config(state=tk.NORMAL)
        guide = open(resource_path("View/text/guide.txt"), "r")
        for line in guide.readlines():
            text += line
        self.text.insert(tk.INSERT, text)
        self.text.config(state=tk.DISABLED)
