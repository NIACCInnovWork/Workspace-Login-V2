"""
NIACC Innovation Workspace Login V2
File that defines the
Author: Anthony Riesen
"""

import tkinter as tk
# from PIL import Image, ImageTK
import datetime as dt
import tkinter.messagebox

import user_interface.sign_in_window
import user_interface.new_user_window
import user_interface.sign_out_window
from database.class_visit import Visit
from database.initialize_database import *


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        date = dt.datetime.now()

        # Create Logged In Frame #####################################################################
        logged_in_frame = tk.LabelFrame(self, text="Logged In")

        # Pull Data
        database = start_workspace_database()
        self.users_logged_in = Visit.get_logged_in_users(database)

        # Create listbox & scrollbar
        scrollbar = tk.Scrollbar(logged_in_frame, orient="vertical")
        self.logged_in_listbox = tk.Listbox(logged_in_frame, yscrollcommand=scrollbar.set, height=15)

        # Populate listbox
        for visitor in self.users_logged_in:
            self.logged_in_listbox.insert(self.users_logged_in.index(visitor), visitor[0])

        # Configure & pack listbox/scrollbar
        scrollbar.config(command=self.logged_in_listbox.yview)
        scrollbar.pack(side="right", fill=tk.Y)
        self.logged_in_listbox.pack(side="left", fill="both", expand=1)
        logged_in_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Create Logo Frame #####################################################################
        logo_frame = tk.LabelFrame(self, text="Workspace Logo")
        photo = tk.PhotoImage(file='resources/Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
        logo_label = tk.Label(logo_frame, image=photo)  # Place Logo into a Label
        logo_label.photo = photo
        logo_label.pack()
        logo_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create Menu Frame #####################################################################
        menu_frame = tk.LabelFrame(self, text="Menu Options")
        sign_in_button = tk.Button(menu_frame, text="Sign In", font=("Arial", 14),
                                   height=3, width=10, command=self.open_sign_in_page)
        new_user_button = tk.Button(menu_frame, text="New User", font=("Arial", 14),
                                    height=3, width=10, command=self.open_new_user_page)
        sign_out_button = tk.Button(menu_frame, text="Sign Out", font=("Arial", 14),
                                    height=3, width=10, command=self.open_sign_out_page)
        sign_in_button.grid(row=0, column=0, padx=10, pady=10)
        new_user_button.grid(row=0, column=1, padx=10, pady=10)
        sign_out_button.grid(row=0, column=2, padx=10, pady=10)
        menu_frame.grid(row=1, column=1, padx=10, pady=10)

        self.grid(row=1, column=0, rowspan=4, columnspan=2)

    def open_sign_in_page(self):
        """
        Opens the SignIn Page Frame within the main window.
        :return: none
        """
        self.destroy()
        user_interface.sign_in_window.SignInPage(self.parent, self.controller)

    def open_new_user_page(self):
        """
        Opens the New User Page Frame within the main window.
        :return:
        """
        self.destroy()
        user_interface.new_user_window.NewUserPage(self.parent, self.controller)

    def open_sign_out_page(self):
        """
        Opens the SignOut Page Frame within the main window if a signed-in user has been selected from the listbox. If
        no users has been selected, a warning popup will appear prompting the user to choose a name to sign out.
        :return:
        """
        try:
            index = self.logged_in_listbox.curselection()
            print(index)
            selected_name = self.logged_in_listbox.get(index)
            selected_id = self.users_logged_in[index[0]][1]
            # print(selected_name)
            self.destroy()
            # user_interface.sign_out_window.SignOutPage(self.parent, self.controller, selected_name)
            user_interface.sign_out_window.SignOutPage(self.parent, self.controller, selected_id)
        except tk.TclError:
            tk.messagebox.showwarning("Select User", "You need to select your name from the list of logged in users!")

