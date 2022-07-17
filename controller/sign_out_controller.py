"""
NIACC Innovation Workspace Login V2
This file defines the controller that controls how the Sign Out Window interacts with the database.  It loads relavant
data from the database when opened and saves data to the database when closed.
Author: Anthony Riesen
"""
from database.class_project import Project
from database.class_user import User
from database.class_visit import Visit
from database.class_visit_project import VisitProject
from database.initialize_database import start_workspace_database


def load_visit_data(user_name: str):
    """
    Loads and returns the relevant data for populating the sign-out page given the username of the person being
    logged out.
    :param user_name: Name of the user being logged out.
    :return: (User Name, User Type, Visit Start Time, Visit ID)
    """
    database = start_workspace_database()
    user = User.load(database, user_name)
    visit = Visit.check_logged_in(database, user.user_id)

    visit_data = (user.name, user.user_type, visit.start_time, visit.visit_id)
    return visit_data


def signout_from_ui(visit_id):
    database = start_workspace_database()
    Visit.sign_out_visit(database, visit_id)
    # VisitProject.create()
    # Project.create()
    # Equipment.create()


