"""
NIACC Innovation Workspace Login V2
This file defines the controller that controls how the Sign Out Window interacts with the database.  It loads relavant
data from the database when opened and saves data to the database when closed.
Author: Anthony Riesen
"""
from database import User, UserRepository
from database import Visit, VisitRepository

from database.class_equipment_material import EquipmentMaterial
from database.class_logout_composite import SignOutComposite
from database.class_project import Project, ProjectType
from database.class_visit_project import VisitProject
from database.initialize_database import start_workspace_database
import tkinter.messagebox

seconds_per_hour = 3600
seconds_per_minute = 60


def load_visit_data(user_id: int):
    """
    Loads and returns the relevant data for populating the sign-out page given the username of the person being
    logged out.
    :param user_id: User_id of the user being logged out
    :return: (User Name, User Type, Visit Start Time, Visit ID)
    """
    database = start_workspace_database()
    user_repo = UserRepository(database)
    visit_repo = VisitRepository(database)

    user = user_repo.load(user_id)  # This is simply used the get the user_id, may not be needed
    visit = visit_repo.check_logged_in(user_id)

    visit_data = (user.name, user.user_type, visit.start_time, visit.visit_id)
    return visit_data


def signout_from_ui(user_name: str, project_frames_list: []):
    """
    Restructured Method: This method now just collects the information needed and passes it to the SignOutComposite
    class to construct all the associated objects.
    :param user_name:
    :param project_frames_list:
    :return:
    """
    database = start_workspace_database()
    # Visit.sign_out_visit(database, visit_id)
    sign_out_object = SignOutComposite.create(database, user_name)

    for project_frame in project_frames_list:
        # Collect Project Info
        if project_frame.selected_project.project_id == 0:
            project_name = project_frame.project_name.get()
            project_description = project_frame.project_description.get()
            project_type = ProjectType[project_frame.project_type_variable.get()]

            project_list_length = sign_out_object.add_project(0, project_name, project_description, project_type,
                                                              database)
            project_index = project_list_length - 1
            # @ToDo - this portion looks strange, check if this is really needed anymore
            print(project_index)
        elif project_frame.selected_project.project_id != 0:
            project_list_length = sign_out_object.add_project(project_frame.selected_project.project_id,
                                                              project_frame.selected_project.project_name,
                                                              project_frame.selected_project.project_description,
                                                              project_frame.selected_project.project_type,
                                                              database)
            project_index = project_list_length - 1
            print(project_index)

        for equipment_frame in project_frame.equipment_frames_list:
            # Collect Usage Info
            equipment_id = equipment_frame.get_equipment_id()
            time_used_hours = equipment_frame.time_used_hours.get()
            if time_used_hours == '':
                time_used_hours = '0'
            time_used_minutes = equipment_frame.time_used_minutes.get()
            if time_used_minutes == '':
                time_used_minutes = '0'
            time_used = (int(time_used_hours) * seconds_per_hour) + (int(time_used_minutes) * seconds_per_minute)
            material_id = equipment_frame.get_material_id()
            amount_consumed = int(equipment_frame.amount_used.get())
            equipment_material_id = EquipmentMaterial.get_equipment_material_id(database, equipment_id, material_id)

            print(project_index, equipment_id, time_used_hours, time_used_minutes,
                  time_used, material_id, equipment_material_id, amount_consumed)
            print(equipment_material_id)

            sign_out_object.add_material_usage(project_index, equipment_material_id, amount_consumed, time_used)

    sign_out_object.commit_data(database)







