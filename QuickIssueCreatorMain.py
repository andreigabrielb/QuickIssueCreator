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
import datetime
import geocoder

#This class will create the main application UI as an object with all of the buttons it requires
class QIC_Main_UI:

    def __init__(self, master):
        #this is the init method for the UI 
        self.master = master
        master.title("Quick Issue creator")
        
        #define the created issues index variable
        self.issue_index = 123

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
        self.create_issue_button = Button(master, text = "Create issue", command = lambda: self.create_issue_UI())
        self.create_issue_button.grid(row = 10)

        #Application close button initialization 
        self.close_app_button = Button(master, text = "Close application", command = master.quit)
        self.close_app_button.grid(row = 10, column = 5)

    #this function defines what happens when a project is selected from project Option menu
    def project_option_function(self, value):
        print value
        print self.project_version_text.get("1.0", "end-1c")
        print self.tester_name_text.get("1.0", "end-1c")
        print self.tested_HW_text.get("1.0", "end-1c")

    #this method will create a new file with the received namea and make that the active file name under use
    def create_new_issue_file(self, name):
        #Assign the value from the issue_file_name_text to the issue_file_name object variable as the active file under use
        if name == '':
            self.message_box_notification("No file name given.")
        else:
            self.issue_file_name = name
            f = open(self.issue_file_name, "w+")
            f.write("Issue ID ||| Time&Date ||| Summary ||| Description ||| GPS coordinates ||| Project ||| project version ||| HW ||| Tester \n")
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

    #This method calls the CreateIssueUI class and passes over all the needed project variable 
    def create_issue_UI(self):
        
        #check if a file to save the issue has been set
        if self.issue_file_name == '':
            self.message_box_notification("No file selected to save the new issue!")
        else:
            #call the class that creates a new issue 
            CreateIssueUI(self.issue_file_name, 
                          self.issue_index, "Ford", 
                          self.project_version_text.get("1.0", "end-1c"), 
                          self.tested_HW_text.get("1.0", "end-1c"), 
                          self.tester_name_text.get("1.0", "end-1c")
                      )

class CreateIssueUI:

    #This method will initialize the UI and workflow to create an issues
    def __init__(self, ifn, iid, pv, pvt, tht, tnt):

        #create a dictionaty to hold all of the issue data 
        self.issue_dictionary = {
                                "file name" : ifn,
                                "issue index" : iid,
                                "project name" : pv,
                                "project version" : pvt,
                                "HW setup" : tht,
                                "tester" : tnt, 
                                "issue summary" : "summary",
                                "issue description" : "description",
                                "issue time" : "time",
                                "issue GPS" : "GPS"
                            }

        #create the Top level that will be the create issue main window 
        self.create_issue_window = Toplevel()
        self.create_issue_window.title("Create issue")

        #issue summary label and text field
        self.issue_summary_label = Label(self.create_issue_window, text = "Summary")
        self.issue_summary_label.grid(row = 1)

        self.issue_summary_text = Text(self.create_issue_window, height = 1, width = 50)
        self.issue_summary_text.insert(END, "Write issue summary here")
        self.issue_summary_text.grid(row = 1, column = 1)

        #create issue description label and text field
        self.issue_description_label = Label(self.create_issue_window, text = "Summary")
        self.issue_description_label.grid(row = 2)

        self.issue_description_text = Text(self.create_issue_window, height = 5, width = 50)
        self.issue_description_text.insert(END, "Write issue description here")
        self.issue_description_text.grid(row = 2, column = 1)

        #Get the time stamps for the created issue
        now = datetime.datetime.now()
        self.issue_datetime_text = Text(self.create_issue_window, height = 1, width = 30)
        self.issue_datetime_text.insert(END, str(now))
        self.issue_datetime_text.grid(row = 3)

        #Get GPS coordinates from the system
        g = geocoder.ip('me')
        print(g.latlng)
        GPScoord = str(g.latlng)

        #Get GPS coordinates (This will be done later)
        self.issue_GPS_text = Text(self.create_issue_window, height = 1, width = 30)
        self.issue_GPS_text.insert(END, GPScoord)
        self.issue_GPS_text.grid(row = 3, column = 1)

        #define the button that will save a created issue and close the window
        self.save_close_issue_button = Button(self.create_issue_window, text = "Save and Close", command = lambda: self.save_issue_method(self.issue_dictionary))
        self.save_close_issue_button.grid(row = 5)

        #define the button that will discard an issue and close the window
        self.save_close_issue_button = Button(self.create_issue_window, text = "Discard", command = self.create_issue_window.destroy)
        self.save_close_issue_button.grid(row = 5, column = 1)

    #This method will save the current data as an new line in the 
    def save_issue_method(self, issue_dict):

        #set the latest issue values to the dictionary
        issue_dict["issue time"] = self.issue_datetime_text.get("1.0", "end-1c")
        issue_dict["issue summary"] = self.issue_summary_text.get("1.0", "end-1c")
        issue_dict["issue description"] = self.issue_description_text.get("1.0", "end-1c")
        issue_dict["issue GPS"] = self.issue_GPS_text.get("1.0", "end-1c")

        #open file for appending a new new issue at the end
        f = open(issue_dict["file name"], "a")

        # Write the "Issue ID ||| Time&Date ||| Summary ||| Description ||| GPS coordinates ||| Project ||| project version ||| HW ||| Tester" values in the file
        f.write("%d ||| %s ||| %s ||| %s ||| %s ||| %s ||| %s ||| %s ||| %s \n" %(issue_dict["issue index"], 
                                                                               issue_dict["issue time"], 
                                                                               issue_dict["issue summary"],
                                                                               issue_dict["issue description"], 
                                                                               issue_dict["issue GPS"],
                                                                               issue_dict["project name"],
                                                                               issue_dict["project version"],
                                                                               issue_dict["HW setup"],
                                                                               issue_dict["tester"]
                                                                               ))
        f.close()
        self.create_issue_window.destroy()

#initialization of the application
if __name__ == "__main__":
    root = Tk()
    app_gui = QIC_Main_UI(root)
    root.mainloop()