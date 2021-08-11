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

    # ! No usage ?
    def emit(self, record):
        # re-enable textfield and insert a message in the console
        self.textfield.config(state=tk.NORMAL)
        # add time log
        time = datetime.now().strftime("%H:%M:%S")
        message = time + "\n" + self.format(record) + "\n\n"
        # add message and log level
        self.textfield.insert(tk.INSERT, message, record.levelname)
        # finally display the message in the textfield
        self.textfield.see(tk.END)
        # disable it again - default state
        self.textfield.config(state=tk.DISABLED)
