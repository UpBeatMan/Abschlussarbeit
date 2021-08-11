import tkinter as tk  # ToolKit module


class DebugDialog(tk.Toplevel):  # toplevel window - console log
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Debugmodus")
        self.resizable(0, 0)
        self.return_value = None

        self.controller = controller

        # a frame to organize other widgets
        self.console_frame = tk.Text(self, width=160)
        # the debug console frame
        self.console = tk.Text(self.console_frame, width=160)
        self.console.config(state=tk.DISABLED)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.hide_button = tk.Button(
            button_frame, text="Verstecken", width=15, command=self.hide
        )

        self.console_frame.pack(side=tk.TOP)
        self.console.pack(side=tk.BOTTOM, fill="x")
        self.hide_button.pack()

    def show(self):
        # * show a hidden tk widget again
        self.wm_deiconify()  # displays the window, after using either the iconify or the withdraw methods
        self.wait_window()  # this method can be called after the event which needs to happen before the window event
        return self.return_value

    def hide(self):
        self.withdraw()
        self.wait_window()

    def close(self):
        self.destroy()
