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
from tkFileDialog import askopenfilename

#This class will create the main application UI as an object with all of the buttons it requires
class QIC_Main_UI:

    def __init__(self, master):
        #this is the init method for the UI 
        self.master = master
        master.title("Quick Issue creator")
        
        #define the created issues index variable
        self.issue_index = 0

        #ser the value of the issue_file_name under use to ""
        self.issue_file_name = ''

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

        #label and text box for the file name that will contain the issues
        self.issue_file_name_label = Label(master, text = "Name of issues file: ")
        self.issue_file_name_label.grid(row = 3)

        self.issue_file_name_text = Text(master, height = 1, width = 30)
        self.issue_file_name_text.insert(END, "File_name.txt")
        self.issue_file_name_text.grid(row = 3, column = 1)

        #create button to load an existing issues file
        self.create_issues_file_button = Button (master, text = "Create issues file", command = lambda: self.create_new_issue_file(self.issue_file_name_text.get("1.0", "end-1c")))
        self.create_issues_file_button.grid(row = 3, column = 2)

        #create button to load an existing issues file
        self.load_issues_file_button = Button (master, text = "Load issues file", command = lambda: self.load_issue_file())
        self.load_issues_file_button.grid(row = 3, column = 3)

        #button that will call a Toplevel UI to create a new issue
        self.create_issue_button = Button(master, text = "Create issue", command = lambda: self.create_issue_method())
        self.create_issue_button.grid(row = 10)

        #Application close button initialization 
        self.close_app_button = Button(master, text = "Close application", command = master.quit)
        self.close_app_button.grid(row = 10, column = 5)
    
    #This method will initialize the UI and workflow to create an issues
    def create_issue_method(self):
        create_issue_window = Toplevel()
        create_issue_window.title("Create issue")

        #issue summary label and text field
        issue_summary_label = Label(create_issue_window, text = "Summary")
        issue_summary_label.grid(row = 1)

        issue_summary_text = Text(create_issue_window, height = 1, width = 50)
        issue_summary_text.insert(END, "Write issue summary here")
        issue_summary_text.grid(row = 1, column = 1)

        #create issue description label and text field
        issue_description_label = Label(create_issue_window, text = "Summary")
        issue_description_label.grid(row = 2)

        issue_description_text = Text(create_issue_window, height = 5, width = 50)
        issue_description_text.insert(END, "Write issue description here")
        issue_description_text.grid(row = 2, column = 1)

        #define the button that will save a created issue
        save_close_issue_button = Button(create_issue_window, text = "Save", command = lambda: self.save_issue_method(create_issue_window))
        save_close_issue_button.grid(row = 5)

        #define the button that will discard an issue and close the window
        save_close_issue_button = Button(create_issue_window, text = "Close", command = create_issue_window.destroy)
        save_close_issue_button.grid(row = 5, column = 1)

    #This method will handle the Save & Close button event
    def save_issue_method(self, ciw):
        print(ciw)
        ciw.destroy

    #this function defines what happens when a project is selected from project Optionmenu
    def project_option_function(self, value):
        print value
        print self.project_version_text.get("1.0", "end-1c")
        print self.tester_name_text.get("1.0", "end-1c")
        print self.tested_HW_text.get("1.0", "end-1c")

    #this method will create a new file with the received namea and make that the active file name under use
    def create_new_issue_file(self, name):
        #Assign the value from the issue_file_name_text to the issue_file_name object variable as the active file under use
        if name == '':
            print"no file name"
            self.message_box_notification("No file name given.")
        else:
            self.issue_file_name = name
            f = open(self.issue_file_name, "w+")
            f.write("This is a test file")
            f.close()
            self.message_box_notification("File %s created" % self.issue_file_name)

    # this method will load an existng issue file as the issue file under use
    def load_issue_file(self):
        #This function will load a file and assign it to the appropriate object variable
        self.issue_file_name = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        self.message_box_notification("File %s loaded" % self.issue_file_name)

    # this method will create a message box and print the passed text
    def message_box_notification(self, txt):
        #crate the top level for message box
        mess_box = Toplevel()
        mess_box.title("Message")
        #create the message text
        msg = Message(mess_box, text = txt)
        msg.pack()
        #create top level close button
        mess_box_close = Button(mess_box, text = "OK", command = mess_box.destroy)
        mess_box_close.pack()

#initialization of the application
if __name__ == "__main__":
    root = Tk()
    app_gui = QIC_Main_UI(root)
    root.mainloop()