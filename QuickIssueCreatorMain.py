
import os.path
import sys
from Tkinter import Tk
from Tkinter import Label
from Tkinter import Button
from Tkinter import Message
from Tkinter import Toplevel

#This class will create the main application UI as an object with all of the buttons it requires
class QIC_Main_UI:

    def __init__(self, master):
        #this is the init method for the UI 
        self.master = master
        master.title("Quick Issue creator")

        self.app_info_label = Label(master, text = "This application is will ment to create quick issues that can then be uploaded to issue tracking tool")
        self.app_info_label.grid(row = 0)

        self.close_app_button = Button(master, text = "Close application", command = master.quit)
        self.close_app_button.grid(row = 10, column = 5)


if __name__ == "__main__":
    root = Tk()
    app_gui = QIC_Main_UI(root)
    root.mainloop()