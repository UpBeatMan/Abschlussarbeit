# ToolKit module
import tkinter as tk


class AskDialog(tk.Toplevel):
    """AskDialog class opens a popup window"""

    # * toplevel - popup confirmation window
    # * a window with text for a question/request, an okay and cancel button
    def __init__(self, parent, controller, text):
        tk.Toplevel.__init__(self, parent)
        self.title("Achtung")
        self.resizable(0, 0)

        self.controller = controller
        self.return_value = None

        tk.Label(self, text=text).pack(side=tk.TOP, pady=10, padx=10)

        # * button area
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        # * button configuration
        self.ok_button = tk.Button(
            button_frame, text="OK", width=10, command=self.on_ok
        )
        self.cancel_button = tk.Button(  # changed from cancle to cancel
            button_frame, text="Abbrechen", width=10, command=self.on_cancel
        )

        # * place(pack) buttons in gui area
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)  # changed from cancle to cancel

    def on_ok(self, event=None):
        """on_ok indicates a positive user decision and closes window"""
        self.return_value = True
        self.destroy()

    def on_cancel(self, event=None):  # changed from cancle to cancel!
        """on_cancel indicates a negative user decision and closes window"""
        self.return_value = False
        self.destroy()

    def show(self):
        """shows a hidden tk widget again"""
        self.wm_deiconify()  # displays the window, after using either the iconify or the withdraw methods
        self.wait_window()  # this method can be called after the event which needs to happen before the window event
        return self.return_value
