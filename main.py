# This application is the updated login system for the NIACC Innovation Workspace.

# Import key libraries
from tkinter import *
import datetime as dt

# Import of additional files
from sign_in_window import *
from new_user_window import *
from sign_out_window import *

# Format the main window
root = Tk()  # Must come first because it defines the window
root.title('Innovation Workspace Login')  # Create title of the window

workspaceLogo = PhotoImage(file='Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
logoLabel = Label(root, image=workspaceLogo)  # Place Logo into a Label

# Implement Datetime
date = dt.datetime.now()

# Creating buttons for the main page
signInButton = Button(root, text="Sign In", font=("Arial", 14),
                      height=5, width=20, command=lambda: open_sign_in(root, date))  # Creating Sign In Button
newUserButton = Button(root, text="New User", font=("Arial", 14),
                       height=5, width=20, command=lambda: open_new_user(root, date))  # Creating New User Button
signOutButton = Button(root, text="Sign Out", font=("Arial", 14),
                       height=5, width=20, command=lambda: open_sign_out(root, date))  # Creating Sign Out Button

# Placing Objects on Screen
logoLabel.grid(row=0, column=0, columnspan=3)
signInButton.grid(row=1, column=0)
newUserButton.grid(row=1, column=1)
signOutButton.grid(row=1, column=2)

root.mainloop()  # Creating an event loop
