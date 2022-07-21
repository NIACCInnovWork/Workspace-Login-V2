"""
NIACC Innovation Workspace Login V2
This file defines the controller that controls how the Sign Out Window interacts with the database.  It loads relavant
data from the database when opened and saves data to the database when closed.
Author: Anthony Riesen
"""
from database.class_project import Project, ProjectType
from database.class_user import User
from database.class_visit import Visit
from database.class_visit_project import VisitProject
from database.initialize_database import start_workspace_database
import tkinter.messagebox


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


def signout_from_ui(visit_id: int, project_frames_list: []):
    database = start_workspace_database()
    Visit.sign_out_visit(database, visit_id)

    for project_frame in project_frames_list:
        # Collect Project Info
        project_name = project_frame.project_name.get()
        project_description = project_frame.project_description.get()
        project_type = ProjectType[project_frame.project_type_variable.get()]

        try:
            project_record = Project.load(database, project_name)
        except TypeError:
            project_record = Project.create(database, project_name, project_description, project_type)
            visit_project_record = VisitProject.create(database, visit_id, project_record.project_id)
        else:
            print("This project already exists.")
            tkinter.messagebox.showwarning("Project Already Exists!",
                                           "The Project Name %s already exists. Please select a different name,"
                                           "and remove any projects that didn't create this error to prevent it "
                                           "from appearing again.")

        # @ToDo - Things to consider
        '''
        1 - Possibly return the indices of all the projects that passed and automatically remove those frames from the UI
            so that only the project that needs correcting remains.
        2 - Possibly adjust the formatting slightly so we can have a "did you mean to add your visit to this existing 
            project, yes/no" option in a popup.
        '''




