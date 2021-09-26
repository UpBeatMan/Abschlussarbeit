from tkinter import *
from PIL import ImageTk, Image

# open new window
root = Tk()
root.title("Learn to open a new windows with TKinter")
root.iconbitmap("C:\\PythonProject\\Abschlussarbeit\\logo\\logo.ico")


def open():
    global my_img
    top = Toplevel()
    top.iconbitmap("C:\\PythonProject\\Abschlussarbeit\\logo\\logo.ico")
    top.title("Hey, look this is our logo!")
    # lbl = Label(top, text="It worked.").pack()
    my_img = ImageTk.PhotoImage(
        Image.open("C:\\PythonProject\\Abschlussarbeit\\logo\\logo_small.png")
    )
    my_label = Label(top, image=my_img).pack()
    btn2 = Button(top, text="close window", command=top.destroy).pack()


btn = Button(root, text="open logo previewer", command=open).pack()

mainloop()
