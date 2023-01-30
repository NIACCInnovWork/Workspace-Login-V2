"""
NIACC Innovation Workspace Login V2
Main file that serves as the starting place for the login application.
Author: Anthony Riesen
"""

import tkinter as tk
import os
from tkinter import font as tkfont

import ws_login_ui.user_interface.launch_gui as launch_gui
from ws_login_client import ApiClient

class LoginApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Workspace Login Application")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        api_client = ApiClient(
                os.environ.get("API_HOST", "https://workspace-login.riesenlabs.com"), 
                os.environ.get("API_TOKEN", "test-token")
        )
        mainframe = launch_gui.MainPage(container, self, api_client)


if __name__ == "__main__":
    # Temporarily Turned off for data analysis -- Runs main application
    app = LoginApplication()
    app.mainloop()
