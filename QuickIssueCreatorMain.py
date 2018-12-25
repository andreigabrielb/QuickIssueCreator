import os.path
import sys
from Tkinter import Tk
from Tkinter import Label
from Tkinter import Button
from Tkinter import Message
from Tkinter import Toplevel
from Tkinter import OptionMenu
from Tkinter import StringVar
from Tkinter import Text
from Tkinter import END

#This class will create the main application UI as an object with all of the buttons it requires
class QIC_Main_UI:

    def __init__(self, master):
        #this is the init method for the UI 
        self.master = master
        master.title("Quick Issue creator")

        #define the created issues index variable
        self.issue_index = 0

        #Application close button initialization 
        self.close_app_button = Button(master, text = "Close application", command = master.quit)
        self.close_app_button.grid(row = 10, column = 5)

        #Project defintion label and text field
        self.project_label = Label(master, text = "Project: ")
        self.project_label.grid(row = 1)

        #define the list of project that can be selected
        project_list = { "None", "FordSyn4", "Vito", "BMW"}
        self.projectVar = StringVar()
        self.projectVar.set("None")
        self.project_option_menu = OptionMenu(master, self.projectVar, *project_list, command = self.project_option_function)
        self.project_option_menu.grid(row = 1, column = 1)

        #Define and initialize a text box field in which the project version can be written
        self.project_version_label = Label(master, text = "Project version: ")
        self.project_version_label.grid(row = 1, column = 2)

        self.project_version_text = Text(master, height = 1, width = 30)
        self.project_version_text.insert(END, "project version no.")
        self.project_version_text.grid(row = 1, column = 3)

        #Define and initialize a text box field in which the tester name can be written
        self.tester_name_label = Label(master, text = "Tester name: ")
        self.tester_name_label.grid(row = 2)

        self.tester_name_text = Text(master, height = 1, width = 30)
        self.tester_name_text.insert(END, "tester name")
        self.tester_name_text.grid(row = 2, column = 1)

        #Define and initialize a text box field in which the hardware under test can be written
        self.tested_HW_label = Label(master, text = "HW used for testing: ")
        self.tested_HW_label.grid(row = 2, column = 2)

        self.tested_HW_text = Text(master, height = 1, width = 30)
        self.tested_HW_text.insert(END, "hw used for testing")
        self.tested_HW_text.grid(row = 2, column = 3)

    #this function defines what happens when a project is selected from project Optionmenu
    def project_option_function(self, value):
        print value
        print self.project_version_text.get("1.0", "end-1c")
        print self.tester_name_text.get("1.0", "end-1c")
        print self.tested_HW_text.get("1.0", "end-1c")

#initialization of the application
if __name__ == "__main__":
    root = Tk()
    app_gui = QIC_Main_UI(root)
    root.mainloop()