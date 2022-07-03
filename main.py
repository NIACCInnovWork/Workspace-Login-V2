
import tkinter as tk
from tkinter import font as tkfont

from user_interface.launch_gui import MainPage
from user_interface.new_user_window import NewUserPage
from user_interface.sign_in_window import SignInPage
from user_interface.sign_out_window import SignOutPage


class LoginApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, NewUserPage, SignInPage, SignOutPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = LoginApplication()
    app.mainloop()




# """
# NIACC Innovation Workspace Login V2
# Main file that serves as the starting place for the login application.
# Author: Anthony Riesen
# """
# from database.initialize_database import *
# from user_interface.launch_gui import LoginApplication
#
# # Initialize Database if it is needed
# create_workspace_database()
# mydb = start_workspace_database()
# create_users_table(mydb)
# create_visits_table(mydb)
#
# application = LoginApplication()
# # application.launch_gui()
# application.mainloop()
