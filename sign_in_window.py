# Sign In Window File

# This file defines the window layout and behavior for signing in to
# the NIACC Innovation Workspace for existing users of the space

from tkinter import *


def open_sign_in(root, date):
    sign_in_window = Toplevel(root)
    sign_in_window.geometry("750x250")
    sign_in_window.title("Sign In Window")

    # Crete Objects
    sign_in_window_title_label = Label(sign_in_window, text="Sign In", font=("Arial", 14), pady=10)
    users_list_box = Listbox(sign_in_window)
    user_name_label = Label(sign_in_window, text="User Name", padx=5)
    user_name_entry = Entry(sign_in_window, state='disabled')

    visit_date_label = Label(sign_in_window, text="Visit DateTime", padx=5)
    visit_date_entry = Entry(sign_in_window)
    visit_date_entry.insert(END, date)

    # Place Objects
    sign_in_window_title_label.grid(row=0, column=0, columnspan=2)
    users_list_box.grid(row=1, column=0, rowspan=3)

    user_name_label.grid(row=1, column=1)
    user_name_entry.grid(row=1, column=2)

    visit_date_label.grid(row=2, column=1)
    visit_date_entry.grid(row=2, column=2)
