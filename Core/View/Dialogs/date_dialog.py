import datetime # handle date and time values
import tkinter as tk # ToolKit module

from dateutil.relativedelta import *
from tkcalendar import DateEntry


class DateDialog(tk.Toplevel):
    """DateDialog class opens a popup window"""

    def __init__(self, parent, controller):
        """run __init__ section at class instantiation"""

        # * create a reference to parent window
        tk.Toplevel.__init__(self, parent)
        # * set window title
        self.title("Änderung via Datum")
        # * lock window size
        self.resizable(0, 0)

        self.controller = controller
        self.return_value = None
        self.date = datetime.datetime.now()

        tk.Label(self, text="Datum auswählen:").pack(side=tk.TOP, pady=8)

        values_frame = tk.Frame(self)
        values_frame.pack(pady=4)

        self.calendar = DateEntry(
            values_frame,
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            locale="de_DE",
        )
        self.calendar.bind("<<DateEntrySelected>>", self.set_new_date)
        self.calendar.pack(pady=6)

        self.labels = {"Stunde": None, "Minute": None, "Sekunde": None}

        for label in self.labels:
            frame = tk.Frame(values_frame)
            frame.pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=label).pack(side=tk.LEFT)
            if label == "Stunde":
                self.labels[label] = tk.Spinbox(frame, from_=0, to=23, width=5)
            else:
                self.labels[label] = tk.Spinbox(frame, from_=0, to=60, width=5)
            self.labels[label].pack(side=tk.RIGHT, padx=2)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=6)

        self.ok_button = tk.Button(
            button_frame, text="Ok", width=10, command=self.on_ok
        )
        self.cancel_button = tk.Button( # changed from cancle_button to cancel_button !
            button_frame, text="Abbrechen", width=10, command=self.on_cancel  # changed from on_cancle to on_cancel !
        )

        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(side=tk.RIGHT, padx=5) # changed from cancle_button to cancel_button !
        self.cancel_button.pack(side=tk.RIGHT, padx=5) 

    def set_new_date(self, e):
        """stores selected date in calendar widget into self.date"""
        self.date = self.calendar.get_date()

    def on_ok(self, event=None):
        """return date and time value on_ok click and close window"""
        self.return_value = datetime.datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            hour=int(self.labels["Stunde"].get()),
            minute=int(self.labels["Minute"].get()),
            second=int(self.labels["Sekunde"].get()),
        )
        self.destroy()

    def on_cancel(self, event=None): # changed from on_cancle to on_cancel !
        """closes window on_cancel click"""
        self.destroy()

    def show(self):
        """shows a hidden tk widget again"""
        # * displays the window, after using either the iconify or the withdraw methods
        self.wm_deiconify()
        # * this method can be called after the event which needs to happen before the window event
        return self.return_value
