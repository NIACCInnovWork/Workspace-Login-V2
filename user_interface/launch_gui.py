"""
NIACC Innovation Workspace Login V2
File that defines the
Author: Anthony Riesen
"""

import tkinter.messagebox
from tkinter import *
import datetime as dt

# Import of additional files
from user_interface.sign_in_window import *
from user_interface.new_user_window import *
from user_interface.sign_out_window import *


def launch_gui():
    """
    Function that starts the main application user interface.
    :return: none
    """
    # Format the main window
    main_window = Tk()  # Must come first because it defines the window
    main_window.title('Innovation Workspace Login')  # Create title of the window

    # def disable_close():
    #     tkinter.messagebox.showinfo("Close Disabled", "The regular exit feature has been disabled to prevent the "
    #                                                   "application from closing prematurely. \n \n "
    #                                                   "Thank you, "
    #                                                   "\n Workspace Staff")
    #
    # root.protocol("WM_DELETE_WINDOW", disable_close)

    workspace_logo = PhotoImage(file='resources/Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
    logo_label = Label(main_window, image=workspace_logo)  # Place Logo into a Label

    # Implement Datetime
    date = dt.datetime.now()

    # Creating buttons for the main page
    sign_in_button = Button(main_window, text="Sign In", font=("Arial", 14),
                            height=3, width=10, command=lambda: open_sign_in(main_window, date))
    new_user_button = Button(main_window, text="New User", font=("Arial", 14),
                             height=3, width=10, command=lambda: open_new_user(main_window, date))
    sign_out_button = Button(main_window, text="Sign Out", font=("Arial", 14),
                             height=3, width=10, command=lambda: open_sign_out(main_window, date))

    # Placing Objects on Screen
    logo_label.grid(row=0, column=0, columnspan=3)
    sign_in_button.grid(row=1, column=0, pady=10)
    new_user_button.grid(row=1, column=1, pady=10)
    sign_out_button.grid(row=1, column=2, pady=10)

    main_window.mainloop()  # Creating an event loop


