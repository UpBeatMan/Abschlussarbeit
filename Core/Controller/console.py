import logging  # logging module for debugging
import tkinter as tk  # tkinter gui module
from datetime import datetime  # module for date and time object


class Console(logging.Handler):
    """a custom logging handler class"""

    def __init__(self, textfield):

        # run the constructor of the Handler class
        logging.Handler.__init__(self)

        # create a textfield defaults
        self.textfield = textfield
        self.textfield.config(state=tk.DISABLED)  # disable textfield

        # set log numerate start value
        self.numerate = 0

        # colorization of the different log levels
        self.textfield.tag_config("INFO", foreground="black")
        self.textfield.tag_config("WARNING", foreground="blue")
        self.textfield.tag_config("DEBUG", foreground="green")
        self.textfield.tag_config("ERROR", foreground="red")
        self.textfield.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        """defines procedure when log messages are send to the log listener"""

        # re-enable textfield and insert a message in the console
        self.textfield.config(state=tk.NORMAL)

        # enumerate log messages
        self.numerate += 1
        if self.numerate < 10:  # adds prefix null for readability
            name = "   - 0" + str(self.numerate) + ".log"
        else:
            name = "   - " + str(self.numerate) + ".log"
        # add timestamp to log
        time = datetime.now().strftime("  %H:%M:%S %d.%m.%y -")
        message = name + time + "\n" + self.format(record) + "\n\n"

        # add message and log level
        self.textfield.insert(tk.INSERT, message, record.levelname)
        # finally display the message in the textfield
        self.textfield.see(tk.END)
        # disable it again - default state
        self.textfield.config(state=tk.DISABLED)
