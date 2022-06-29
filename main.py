"""
NIACC Innovation Workspace Login V2
Main file that serves as the starting place for the login application.
Author: Anthony Riesen
"""
from database.initialize_database import *
from user_interface.launch_gui import launch_gui

# Initialize Database if it is needed
create_workspace_database()
mydb = start_workspace_database()
create_users_table(mydb)
create_visits_table(mydb)

launch_gui()
