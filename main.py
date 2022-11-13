"""
NIACC Innovation Workspace Login V2
Main file that serves as the starting place for the login application.
Author: Anthony Riesen
"""


import tkinter as tk
from tkinter import font as tkfont
from database.initialize_database import *

import user_interface.launch_gui
from reports.generate_KPI_report import generate_kpi_report
from reports.generate_pdf_report import construct_pdf, ReportPDF, generate_full_report
from reports.pandas_exploration import run_report
from reports.total_report import generate_total_report
from reports.weekly_report import generate_weekly_report


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
    # run_report(mydb)  # This function is deprecated and going to be removed
    generate_total_report(mydb)
    # generate_kpi_report() # This function generates the PDF and is turned off as plots are being developed

    # Temporarily Turned off for data analysis -- Runs main application
    # app = LoginApplication()
    # app.mainloop()
