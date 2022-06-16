# New User Window File

# This file defines the window layout and behavior for creating a new user for
# the NIACC Innovation Workspace login application

from tkinter import *


def open_new_user(root, date):  # Function to open new user window
    new_user_window = Toplevel(root)
    new_user_window.title("New User Window")

    # Create objects
    new_user_window_title_label = Label(new_user_window, text="Enter the information below to create a new user",
                                        font=("Arial", 14), pady=10)
    name_entry_label = Label(new_user_window, text="Full Name", pady=5)
    name_entry = Entry(new_user_window)

    is_student_checkbox = Checkbutton(new_user_window, text='Student')
    is_entrepreneur_checkbox = Checkbutton(new_user_window, text='Entrepreneur')
    is_community_checkbox = Checkbutton(new_user_window, text='Community Member')

    submit_new_user_button = Button(new_user_window, text='Submit New User')

    # Place objects
    new_user_window_title_label.grid(row=0, column=0, columnspan=3)
    name_entry_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    is_student_checkbox.grid(row=2, column=0)
    is_entrepreneur_checkbox.grid(row=2, column=1)
    is_community_checkbox.grid(row=2, column=2)
    submit_new_user_button.grid(row=3, column=1)
