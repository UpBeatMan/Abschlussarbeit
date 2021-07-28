import logging  # logging module for debugging
import tkinter as tk  # tkinter gui module
from datetime import datetime  # module for date and time object


class Console(logging.Handler):
    def __init__(self, textfield):
        logging.Handler.__init__(self)
        self.textfield = textfield
        self.textfield.config(state=tk.DISABLED)

        # colorization of the different log levels
        self.textfield.tag_config("INFO", foreground="black")
        self.textfield.tag_config("DEBUG", foreground="grey")
        self.textfield.tag_config("WARNING", foreground="orange")
        self.textfield.tag_config("ERROR", foreground="red")
        self.textfield.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        # insert a message into the console
        self.textfield.config(state=tk.NORMAL)

        time = datetime.now().strftime("%H:%M:%S")
        message = time + "\n" + self.format(record) + "\n\n"

        self.textfield.insert(tk.INSERT, message, record.levelname)
        self.textfield.see(tk.END)
        self.textfield.config(state=tk.DISABLED)
