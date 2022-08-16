"""
NIACC Innovation Workspace Login V2
Main file that serves as the starting place for the login application.
Author: Anthony Riesen
"""


import tkinter as tk
from tkinter import font as tkfont
from database.initialize_database import *

import user_interface.launch_gui


class LoginApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Workspace Login Application")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        mainframe = user_interface.launch_gui.MainPage(container, self)


if __name__ == "__main__":
    create_workspace_database()
    mydb = start_workspace_database()
    create_users_table(mydb)
    create_visits_table(mydb)
    create_projects_table(mydb)
    create_visits_projects_table(mydb)
    create_usage_log_table(mydb)
    create_equipment_table(mydb)
    create_materials_table(mydb)
    create_equipment_materials_table(mydb)
    create_materials_consumed_table(mydb)
    app = LoginApplication()
    app.mainloop()
