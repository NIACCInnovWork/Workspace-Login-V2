# Sign Out Window File

# This file defines the window layout and behavior for signing out of
# the NIACC Innovation Workspace for logged-in users of the space
"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the Sign Out window.
Author: Anthony Riesen
"""
from tkinter import *


def open_sign_out(root, date):  # Function to open sign out window
    """
    Function to create Sign Out window upon button click
    :param root: Primary TK Object (main_window)
    :param date: Not currently being used @todo remove
    :return: none
    """
    sign_out_window = Toplevel(root)
    # sign_out_window.geometry("750x250")
    sign_out_window.title("Sign Out Window")

    # Functions
    def exit_button():
        sign_out_window.destroy()
        sign_out_window.update()

    # Create Objects
    logged_in_title = Label(sign_out_window, text="User Sign Out", font=("Arial", 14))
    logged_in_users = Listbox(sign_out_window, width=30, height=15)

    user_name_label = Label(sign_out_window, text="User Name:", padx=5)
    user_name_entry = Entry(sign_out_window, width=30, state="disabled")

    visit_date_label = Label(sign_out_window, text="Visit DateTime:", padx=5)
    visit_date_entry = Entry(sign_out_window, width=30)
    visit_date_entry.insert(END, date)
    visit_date_entry.config(state="disabled")

    visitor_type_label = Label(sign_out_window, text="Visitor Type:", padx=5)
    visitor_type_entry = Entry(sign_out_window, width=30, state="disabled")

    equipment_used_label = Label(sign_out_window, text="Equipment Used:", padx=5)
    fdm_3d_printer_checkbox = Checkbutton(sign_out_window, text="FDM 3D Printer")
    sla_3d_printer_checkbox = Checkbutton(sign_out_window, text="SLA 3D Printer")
    laser_cutter_checkbox = Checkbutton(sign_out_window, text="Laser Cutter")
    vinyl_cutter_checkbox = Checkbutton(sign_out_window, text="Vinyl Cutter")
    cnc_mill_checkbox = Checkbutton(sign_out_window, text="CNC Mill")
    robotics_checkbox = Checkbutton(sign_out_window, text="Robotics")
    electronics_checkbox = Checkbutton(sign_out_window, text="Electronics Bench")

    submit_sign_out_button = Button(sign_out_window, text="Sign Out", width=10)
    cancel_sign_out_button = Button(sign_out_window, text="Cancel", width=10, command=exit_button)

    # Place Objects
    logged_in_title.grid(row=0, column=0)
    logged_in_users.grid(row=1, column=0, rowspan=8, padx=10, pady=10)

    user_name_label.grid(row=1, column=1, sticky=E)
    user_name_entry.grid(row=1, column=2, padx=(5, 20))

    visit_date_label.grid(row=2, column=1, sticky=E)
    visit_date_entry.grid(row=2, column=2, padx=(5, 20))

    visitor_type_label.grid(row=3, column=1, sticky=E)
    visitor_type_entry.grid(row=3, column=2, padx=(5, 20))

    equipment_used_label.grid(row=4, column=1, sticky=E)
    fdm_3d_printer_checkbox.grid(row=4, column=2, sticky=W)
    sla_3d_printer_checkbox.grid(row=5, column=2, sticky=W)
    laser_cutter_checkbox.grid(row=6, column=2, sticky=W)
    vinyl_cutter_checkbox.grid(row=7, column=2, sticky=W)
    cnc_mill_checkbox.grid(row=8, column=2, sticky=W)
    robotics_checkbox.grid(row=9, column=2, sticky=W)
    electronics_checkbox.grid(row=10, column=2, sticky=W)

    submit_sign_out_button.grid(row=9, column=3, padx=10)
    cancel_sign_out_button.grid(row=10, column=3, padx=10, pady=(0, 10))

