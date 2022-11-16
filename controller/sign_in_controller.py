"""
NIACC Innovation Workspace Login V2
This file defines the controller that creates new visits by receiving data from the user interface and pulling it from
database for an existing user and pushing it to the database.
Author: Anthony Riesen
"""
import tkinter.messagebox

from database.class_visit import Visit, VisitRepository
from database.initialize_database import start_workspace_database


def create_visit_from_ui(user_id: int):
    database = start_workspace_database()
    visit_repo = VisitRepository(database)
    try:
        visit = visit_repo.check_logged_in(user_id)
    except TypeError:
        visit = Visit.create(database, user_id)
        tkinter.messagebox.showinfo("Logged In!",
                                    "You are all logged in and good to go!")
    else:
        print("You are already logged in.")
        tkinter.messagebox.showwarning("Member Already Logged In!",
                                       "You are already logged in. Please log out instead. \n\n"
                                       "If you forgot to log out previously, please talk to Workspace Staff.")
