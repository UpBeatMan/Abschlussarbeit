import logging  # logging module for debugging
import tkinter as tk  # tkinter gui module
from datetime import datetime  # date and time module


class Console(logging.Handler):
    """a custom logging handler class for event logger"""

    def __init__(self, textfield):

        # * run the constructor of the Handler class
        logging.Handler.__init__(self)

        # * create a textfield defaults
        self.textfield = textfield
        self.textfield.config(state=tk.DISABLED)  # disable textfield

        # * colorization of the different log levels only for event_logger
        self.textfield.tag_config("INFO", foreground="black")
        self.textfield.tag_config("WARNING", foreground="blue")

        # DEBUG, ERROR and CRITICAL log levels only show all details in advanced.log
        # They are handled by the debug_logger without tk colorization
        self.textfield.tag_config("DEBUG", foreground="green")
        self.textfield.tag_config("ERROR", foreground="red")
        self.textfield.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        """defines procedure when log messages are send to the log listener and displayed in the event console"""

        # * re-enable textfield and insert a message in the console
        self.textfield.config(state=tk.NORMAL)

        # * add timestamp to log
        time = datetime.now().strftime("      %H:%M:%S")
        message = time + "            " + self.format(record) + "\n\n"

        # * add message and log level
        self.textfield.insert(tk.INSERT, message, record.levelname)

        # * finally display the message in the textfield
        self.textfield.see(tk.END)

        # * disable textfield again - default state
        self.textfield.config(state=tk.DISABLED)
