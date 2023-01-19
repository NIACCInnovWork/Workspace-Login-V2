"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the New User window.
Author: Anthony Riesen
"""

import tkinter as tk

import user_interface.launch_gui
from controller.new_user_controller import create_user_from_ui
import user_interface.launch_gui


from client import ApiClient

class NewUserPage(tk.Frame):

    def __init__(self, parent, controller, api_client: ApiClient):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.api_client = api_client

        new_user_window_title_label = tk.Label(self, text="Create User", font=("Arial", 14), pady=10)
        name_entry_label = tk.Label(self, text="Full Name:", pady=5)
        name_entry = tk.Entry(self, width=30)

        member_type_label = tk.Label(self, text="Member Type:")
        user_type_id = tk.IntVar()
        is_student_checkbox = tk.Radiobutton(self, text="Student", pady=5, value=1, variable=user_type_id)
        is_student_checkbox.select()
        is_staff_checkbox = tk.Radiobutton(self, text="Staff", pady=5, value=2, variable=user_type_id)
        is_entrepreneur_checkbox = tk.Radiobutton(self, text="Entrepreneur", pady=5, value=3, variable=user_type_id)
        is_business_checkbox = tk.Radiobutton(self, text="Business Member", pady=5, value=4, variable=user_type_id)
        is_community_checkbox = tk.Radiobutton(self, text="Community Member", pady=5, value=5, variable=user_type_id)

        def get_new_user_info():
            """
            Pulls new user data from UI and converts user_type to the proper enum before calling controller to create a
            new user with this data.
            :return: none
            """
            name = name_entry.get()

            if user_type_id.get() == 1:
                user_type = "Student"
            elif user_type_id.get() == 2:
                user_type = "Staff"
            elif user_type_id.get() == 3:
                user_type = "Entrepreneur"
            elif user_type_id.get() == 4:
                user_type = "Business_Member"
            elif user_type_id.get() == 5:
                user_type = "Community_Member"
            else:
                user_type = ''  # This should indicate an error of some kind has occurred.

            create_user_from_ui(self.api_client, name, user_type)
            self.return_to_main()
            # controller.show_frame("MainPage")

        submit_new_user_button = tk.Button(self, text="Create User", width=10, command=get_new_user_info)
        cancel_new_user_button = tk.Button(self, text="Cancel", width=10, command=self.return_to_main)

        # Place objects
        new_user_window_title_label.grid(row=0, column=0, columnspan=4)
        name_entry_label.grid(row=1, column=0, sticky="E")
        name_entry.grid(row=1, column=1, columnspan=2, sticky="W")

        member_type_label.grid(row=2, column=0)
        is_student_checkbox.grid(row=2, column=1, sticky="W")
        is_staff_checkbox.grid(row=3, column=1, sticky="W")
        is_entrepreneur_checkbox.grid(row=2, column=2, sticky="W")
        is_business_checkbox.grid(row=3, column=2, sticky="W")
        is_community_checkbox.grid(row=2, column=3, sticky="W")

        submit_new_user_button.grid(row=4, column=3)
        cancel_new_user_button.grid(row=5, column=3, pady=(0, 10))

        self.grid(row=0, column=0)

    def return_to_main(self):
        self.destroy()
        user_interface.launch_gui.MainPage(self.parent, self.controller, self.api_client)


#
# def open_new_user(root, date):  # Function to open new user window
#     """
#     Function to create new user window upon button click
#     :param root: Primary TK Object (main_window)
#     :param date: Not currently being used @todo remove
#     :return: none
#     """
#     new_user_window = Toplevel(root)
#     new_user_window.title("New User Window")
#
#     # Create Functions
#     def exit_button():
#         new_user_window.destroy()
#         new_user_window.update()
#
#     def get_new_user_info():
#         """
#         Pulls new user data from UI and converts user_type to the proper enum before calling controller to create a
#         new user with this data.
#         :return: none
#         """
#         name = name_entry.get()
#
#         if user_type_id.get() == 1:
#             user_type = "Student"
#         elif user_type_id.get() == 2:
#             user_type = "Staff"
#         elif user_type_id.get() == 3:
#             user_type = "Entrepreneur"
#         elif user_type_id.get() == 4:
#             user_type = "Business_Member"
#         elif user_type_id.get() == 5:
#             user_type = "Community_Member"
#         else:
#             user_type = ''  # This should indicate an error of some kind has occurred.
#
#         create_user_from_ui(name, user_type)
#         exit_button()
#
#     # Create objects
#
