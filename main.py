from database.initialize_database import *
from user_interface.launch_gui import launch_gui

# Initialize Database if it is needed
create_workspace_database()
mydb = start_workspace_database()
create_users_table(mydb)

launch_gui()
