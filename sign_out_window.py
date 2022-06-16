# Sign Out Window File

# This file defines the window layout and behavior for signing out of
# the NIACC Innovation Workspace for logged-in users of the space

from tkinter import *


def open_sign_out(root, date):  # Function to open sign out window
    sign_out_window = Toplevel(root)
    sign_out_window.geometry("750x250")
    sign_out_window.title("Sign Out Window")

    logged_in_title = Label(sign_out_window, text="Sign Out Here")
    logged_in_users = Listbox(sign_out_window)

    logged_in_title.grid(row=0, column=0, columnspan=2)
    logged_in_users.grid(row=1, column=0)
