# This application is the updated login system for the NIACC Innovation Workspace.

# Import key libraries
import tkinter.messagebox
from tkinter import *
import datetime as dt

# Import of additional files
from user_interface.sign_in_window import *
from user_interface.new_user_window import *
from user_interface.sign_out_window import *


def launch_gui():

    # Format the main window
    root = Tk()  # Must come first because it defines the window
    root.title('Innovation Workspace Login')  # Create title of the window

    def disable_close():
        tkinter.messagebox.showinfo("Close Disabled", "The regular exit feature has been disabled to prevent the "
                                                      "application from closing prematurely. \n \n "
                                                      "Thank you, "
                                                      "\n Workspace Staff")

    root.protocol("WM_DELETE_WINDOW", disable_close)

    workspace_logo = PhotoImage(file='resources/Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
    logo_label = Label(root, image=workspace_logo)  # Place Logo into a Label

    # Implement Datetime
    date = dt.datetime.now()

    # Creating buttons for the main page
    sign_in_button = Button(root, text="Sign In", font=("Arial", 14),
                            height=3, width=10, command=lambda: open_sign_in(root, date))  # Creating Sign In Button
    new_user_button = Button(root, text="New User", font=("Arial", 14),
                             height=3, width=10, command=lambda: open_new_user(root, date))  # Creating New User Button
    sign_out_button = Button(root, text="Sign Out", font=("Arial", 14),
                             height=3, width=10, command=lambda: open_sign_out(root, date))  # Creating Sign Out Button

    # Placing Objects on Screen
    logo_label.grid(row=0, column=0, columnspan=3)
    sign_in_button.grid(row=1, column=0, pady=10)
    new_user_button.grid(row=1, column=1, pady=10)
    sign_out_button.grid(row=1, column=2, pady=10)

    root.mainloop()  # Creating an event loop


