# ToolKit module
import tkinter as tk

# dateutil extension to datetime module
from dateutil.relativedelta import *


class TimedeltaDialog(tk.Toplevel):
    """TimedeltaDialog class opens a popup window"""

    def __init__(self, parent, controller):
        """run __init__ section at class instantiation"""

        # * create a reference to parent window
        tk.Toplevel.__init__(self, parent)
        # * set window title
        self.title("Änderung via Zeitverschiebung")
        # * lock window size
        self.resizable(0, 0)

        self.controller = controller
        self.return_value = None
        self.mode = tk.IntVar()  # 0 for backwards and 1 for forward

        self.labels = {
            "Jahre": None,
            "Monate": None,
            "Tage": None,
            "Stunden": None,
            "Minuten": None,
            "Sekunden": None,
        }

        tk.Label(self, text="Zeitverscheibung auswählen:").pack(side=tk.TOP, pady=8)

        radio_frame = tk.Frame(self)
        radio_frame.pack(pady=3)

        tk.Radiobutton(radio_frame, text="Vor", value=1, variable=self.mode).pack(
            side=tk.LEFT, padx=4
        )
        back_button = tk.Radiobutton(
            radio_frame, text="Zurück", value=0, variable=self.mode
        )
        back_button.select()
        back_button.pack(side=tk.LEFT)

        values_frame = tk.Frame(self)
        values_frame.pack(pady=5)
        for label in self.labels:
            frame = tk.Frame(values_frame)
            frame.pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            self.labels[label] = tk.Spinbox(frame, from_=0, to=99, width=5)
            self.labels[label].pack(side=tk.RIGHT, padx=2)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        self.ok_button = tk.Button(
            button_frame, text="Ok", width=10, command=self.on_ok
        )
        self.cancel_button = tk.Button(  # changed from cancle_button to cancel_button !
            button_frame,
            text="Abbrechen",
            width=10,
            command=self.on_cancel,  # changed from on_cancle to on_cancel !
        )

        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(
            side=tk.RIGHT, padx=5
        )  # changed from cancle_button to cancel_button !

    def on_ok(self, event=None):
        """returns relative date and time value in future or past on_ok click"""
        if self.mode.get() == 0:  # relative date and time in future
            self.return_value = relativedelta(
                years=int(self.labels["Jahre"].get()),
                months=int(self.labels["Monate"].get()),
                days=int(self.labels["Tage"].get()),
                hours=int(self.labels["Stunden"].get()),
                minutes=int(self.labels["Minuten"].get()),
                seconds=int(self.labels["Sekunden"].get()),
            )
        else:  # relative date and time in past
            self.return_value = relativedelta(
                years=int(self.labels["Jahre"].get()) * (-1),
                months=int(self.labels["Monate"].get()) * (-1),
                days=int(self.labels["Tage"].get()) * (-1),
                hours=int(self.labels["Stunden"].get()) * (-1),
                minutes=int(self.labels["Minuten"].get()) * (-1),
                seconds=int(self.labels["Sekunden"].get()) * (-1),
            )

        self.destroy()

    def on_cancel(self, event=None):  # changed from on_cancle to on_cancel !
        """closes window on_cancel click"""
        self.destroy()

    def show(self):
        """shows a hidden tk widget again"""
        # * displays the window, after using either the iconify or the withdraw methods
        self.wm_deiconify()
        # * this method can be called after the event which needs to happen before the window event
        self.wait_window()
        return self.return_value
