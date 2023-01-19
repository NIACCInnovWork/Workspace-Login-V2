"""
NIACC Innovation Workspace Login V2
Main file that serves as the starting place for the login application.
Author: Anthony Riesen
"""

import tkinter as tk
from tkinter import font as tkfont
# from database.initialize_database import *

import user_interface.launch_gui

from client import ApiClient

class LoginApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Workspace Login Application")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        mainframe = user_interface.launch_gui.MainPage(container, self, ApiClient("http://workspace-login.riesenlabs.com"))


if __name__ == "__main__":
    # Temporarily Turned off for data analysis -- Runs main application
    app = LoginApplication()
    app.mainloop()
