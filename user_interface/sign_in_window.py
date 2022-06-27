"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the Sign In window.
Author: Anthony Riesen
"""
from tkinter import *


def open_sign_in(root, date):
    """
    Function to create Sign In window upon button click
    :param root: Primary TK Object (main_window)
    :param date: Not currently being used @todo remove
    :return: none
    """
    sign_in_window = Toplevel(root)
    # sign_in_window.geometry("750x300")
    sign_in_window.title("Sign In Window")

    # Functions
    def exit_button():
        sign_in_window.destroy()
        sign_in_window.update()

    # Crete Objects
    sign_in_window_title_label = Label(sign_in_window, text="User Sign In", font=("Arial", 14), pady=5)
    users_list_box = Listbox(sign_in_window, width=30, height=15)

    user_name_label = Label(sign_in_window, text="User Name:", padx=5)
    user_name_entry = Entry(sign_in_window, width=30, state="disabled")

    visit_date_label = Label(sign_in_window, text="Visit DateTime:", padx=5)
    visit_date_entry = Entry(sign_in_window, width=30)
    visit_date_entry.insert(END, date)
    visit_date_entry.config(state="disabled")

    visitor_type_label = Label(sign_in_window, text="Visitor Type:", padx=5)
    visitor_type_entry = Entry(sign_in_window, width=30, state="disabled")

    purpose_label = Label(sign_in_window, text="Visit Purpose:", padx=5, justify="left")
    purpose_prototyping_checkbox = Checkbutton(sign_in_window, text="Prototyping", justify="left")
    purpose_class_project_checkbox = Checkbutton(sign_in_window, text="Class Project", justify="left")
    purpose_personal_project_checkbox = Checkbutton(sign_in_window, text="Personal Project", justify="left")
    purpose_community_build_checkbox = Checkbutton(sign_in_window, text="Community Build", justify="left")
    purpose_hanging_out_checkbox = Checkbutton(sign_in_window, text="Hanging Out", justify="left")
    purpose_work_study_checkbox = Checkbutton(sign_in_window, text="Work Study", justify="left")

    submit_sign_in_button = Button(sign_in_window, text="Sign In", width=10)
    cancel_sign_in_button = Button(sign_in_window, text="Cancel", width=10, command=exit_button)

    # Place Objects
    sign_in_window_title_label.grid(row=0, column=0)
    users_list_box.grid(row=1, column=0, rowspan=8, padx=(10, 10))

    user_name_label.grid(row=1, column=1, sticky=E)
    user_name_entry.grid(row=1, column=2, padx=(5, 20))

    visit_date_label.grid(row=2, column=1, sticky=E)
    visit_date_entry.grid(row=2, column=2, padx=(5, 20))

    visitor_type_label.grid(row=3, column=1, sticky=E)
    visitor_type_entry.grid(row=3, column=2, padx=(5, 20))

    purpose_label.grid(row=4, column=1, sticky=W)
    purpose_prototyping_checkbox.grid(row=4, column=2, sticky=W, padx=(15, 10))
    purpose_class_project_checkbox.grid(row=5, column=2, sticky=W, padx=(15, 10))
    purpose_personal_project_checkbox.grid(row=6, column=2, sticky=W, padx=(15, 10))
    purpose_community_build_checkbox.grid(row=7, column=2, sticky=W, padx=(15, 10))
    purpose_hanging_out_checkbox.grid(row=8, column=2, sticky=W, padx=(15, 10))
    purpose_work_study_checkbox.grid(row=9, column=2, sticky=W, padx=(15, 10))

    submit_sign_in_button.grid(row=8, column=3, padx=10)
    cancel_sign_in_button.grid(row=9, column=3, padx=10, pady=(0, 10))

