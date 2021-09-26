from tkinter.ttk import Progressbar, Style
from tkinter import Tk, Label
from time import sleep


class LoadingSplash:
    def __init__(self):
        # setting root window:
        self.root = Tk()
        self.root.title("Progressbar")
        self.root.config()  # bg="#1F2732"
        # self.root.attributes("-fullscreen", True)
        self.root.geometry("560x380+300+150")

        # progressbar theme:
        theme = Style()
        theme.theme_use("winnative")
        theme.configure("green.Horizontal.TProgressbar", background="green")

        # loading text:
        txt = Label(self.root, text="Loading...", fg="green")  # bg="#1F2732"
        txt.place(x=200, y=140)
        # txt.place(x=520, y=330)

        # progressbar:
        self.bar = Progressbar(
            self.root,
            style="green.Horizontal.TProgressbar",
            orient="horizontal",
            mode="indeterminate",
            length="180",
        )
        self.bar.place(x=200, y=170)
        # self.bar.place(x=500, y=360)

        # update root to see animation:
        self.root.update()
        self.play_animation()

        # window in mainloop:
        self.root.mainloop()

    # progressbar animation:
    def play_animation(self):
        for i in range(2000):
            self.bar["value"] += 1
            self.root.update_idletasks()
            sleep(0.01)
        else:
            self.root.destroy()
            exit(0)


if __name__ == "__main__":
    LoadingSplash()
