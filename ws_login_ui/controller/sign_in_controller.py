"""
NIACC Innovation Workspace Login V2
This file defines the controller that creates new visits by receiving data from the user interface and pulling it from
database for an existing user and pushing it to the database.
Author: Anthony Riesen
"""
import tkinter.messagebox

# from database.initialize_database import start_workspace_database

from ws_login_client import ApiClient
from ws_login_domain import Visit

def create_visit_from_ui(api_client: ApiClient, user_id: int):
    # database = start_workspace_database()
    # visit_repo = VisitRepository(database)
    user = api_client.get_user(user_id)
    ongoing_visits = api_client.get_visits_for(user, ongoing=True)

    if not ongoing_visits:
        # visit = Visit.create(database, user_id)
        visit = api_client.create_visit_for(user)
        tkinter.messagebox.showinfo("Logged In!",
                                    "You are all logged in and good to go!")
    else:
        print("You are already logged in.")
        tkinter.messagebox.showwarning("Member Already Logged In!",
                                       "You are already logged in. Please log out instead. \n\n"
                                       "If you forgot to log out previously, please talk to Workspace Staff.")
