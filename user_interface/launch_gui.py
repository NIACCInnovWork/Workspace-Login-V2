"""
NIACC Innovation Workspace Login V2
File that defines the
Author: Anthony Riesen
"""

from tkinter import *
# from PIL import Image, ImageTK
import datetime as dt
from user_interface.sign_in_window import *
from user_interface.new_user_window import *
from user_interface.sign_out_window import *
from database.class_visit import Visit
from database.initialize_database import *


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        date = dt.datetime.now()

        # Create Logged In Frame #####################################################################
        logged_in_frame = tk.LabelFrame(self, text="Logged In")

        # Pull Data
        database = start_workspace_database()
        users_logged_in = Visit.get_logged_in_users(database)

        # Create listbox & scrollbar
        scrollbar = tk.Scrollbar(logged_in_frame, orient="vertical")
        logged_in_listbox = tk.Listbox(logged_in_frame, yscrollcommand=scrollbar.set, height=15)

        # Populate listbox
        for name in users_logged_in:
            logged_in_listbox.insert(users_logged_in.index(name), name[0])

        # Configure & pack listbox/scrollbar
        scrollbar.config(command=logged_in_listbox.yview)
        scrollbar.pack(side="right", fill=Y)
        logged_in_listbox.pack(side="left", fill="both", expand=1)
        logged_in_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Create Logo Frame #####################################################################
        logo_frame = LabelFrame(self, text="Workspace Logo")
        photo = PhotoImage(file='resources/Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
        logo_label = Label(logo_frame, image=photo)  # Place Logo into a Label
        logo_label.photo = photo
        logo_label.pack()
        logo_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create Menu Frame #####################################################################
        menu_frame = LabelFrame(self, text="Menu Options")
        sign_in_button = Button(menu_frame, text="Sign In", font=("Arial", 14),
                                height=3, width=10, command=lambda: controller.show_frame("SignInPage"))
        new_user_button = Button(menu_frame, text="New User", font=("Arial", 14),
                                 height=3, width=10, command=lambda: controller.show_frame("NewUserPage"))
        sign_out_button = Button(menu_frame, text="Sign Out", font=("Arial", 14),
                                 height=3, width=10, command=lambda: controller.show_frame("SignOutPage"))
        sign_in_button.grid(row=0, column=0, padx=10, pady=10)
        new_user_button.grid(row=0, column=1, padx=10, pady=10)
        sign_out_button.grid(row=0, column=2, padx=10, pady=10)
        menu_frame.grid(row=1, column=1, padx=10, pady=10)

        self.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=N+S+E+W)
