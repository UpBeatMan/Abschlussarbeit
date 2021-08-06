import os
import getpass

import tkinter as tk
from tkinter import ttk

current_username = getpass.getuser()
print(current_username)

profile_path = (
    "C:/Users/"
    + current_username
    + "/AppData/Local/Google/Chrome/User Data/"
    + "Default/"
)
file_name = "History"

print(profile_path + file_name)


class SampleApp(tk.Tk):
    def __init__(self, profile_path: str, file_name: str, *args, **kwargs):
        if profile_path is None:
            # raise ValueError("profile")
            return
        self.size = os.stat(profile_path + file_name).st_size
        self.maxbytes = 0
        self.bytes = 0

        tk.Tk.__init__(self, *args, **kwargs)
        self.button = ttk.Button(text="start", command=self.start)
        self.button.pack()
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="determinate"
        )
        self.progress.pack()

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = self.size
        self.progress["maximum"] = self.size
        self.read_bytes()

    def read_bytes(self):
        """simulate reading 500 bytes; update progress bar"""
        self.bytes += 500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)


app = SampleApp(profile_path, file_name)
app.mainloop()
