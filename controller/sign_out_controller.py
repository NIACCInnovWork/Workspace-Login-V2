"""
NIACC Innovation Workspace Login V2
This file defines the controller that controls how the Sign Out Window interacts with the database.  It loads relavant
data from the database when opened and saves data to the database when closed.
Author: Anthony Riesen
"""
from client import ApiClient
from database.class_user import User, UserRepository
from database.class_visit import Visit, VisitRepository

from database.class_equipment_material import EquipmentMaterial
from database.class_logout_composite import SignOutComposite
from database.class_project import Project, ProjectType
from database.class_visit_project import VisitProject

import tkinter.messagebox

from dataclasses import dataclass

from flaskr.visit_routes import SignoutRequest

import datetime as dt

seconds_per_hour = 3600
seconds_per_minute = 60


def load_visit_data(user_id: int):
    """
    Loads and returns the relevant data for populating the sign-out page given the username of the person being
    logged out.
    :param user_id: User_id of the user being logged out
    :return: (User Name, User Type, Visit Start Time, Visit ID)
    """
    # database = start_workspace_database()
    user_repo = UserRepository(None)
    visit_repo = VisitRepository(None)

    user = user_repo.load(user_id)  # This is simply used the get the user_id, may not be needed
    visit = visit_repo.check_logged_in(user_id)

    visit_data = (user.name, user.user_type, visit.start_time, visit.visit_id)
    return visit_data


def zero_if_empty(raw: str) -> int:
    if raw == '' or raw is None:
        return 0
    return int(raw)

def signout_from_ui(api_client: ApiClient, visit: Visit, project_frames_list: []):
    """
    Restructured Method: This method now just collects the information needed and passes it to the SignOutComposite
    class to construct all the associated objects.
    :param user_name:
    :param project_frames_list:
    :return:
    """
    print("Signing out from ui")
    sign_out_request = SignoutRequest.for_visit(visit)

    for project_frame in project_frames_list:
        # Collect Project Info
        print("Selected Project")
        print(project_frame.selected_project)
        selected_project = project_frame.selected_project
        if selected_project.project_id == 0 or selected_project.project_id is None:
            work_session = sign_out_request.with_new_project(
                project_frame.project_name.get(),
                project_frame.project_description.get(),
                ProjectType[project_frame.project_type_variable.get()],
            )
        elif selected_project.project_id != 0:
            work_session = sign_out_request.with_existing_project(selected_project)

        for equipment_frame in project_frame.equipment_frames_list:
            # Collect Usage Info
            selected_equipment = equipment_frame.get_equipment()

            time_used = dt.timedelta(
                hours=zero_if_empty(equipment_frame.time_used_hours.get()),
                minutes=zero_if_empty(equipment_frame.time_used_minutes.get())
            )

            eq_use_log = work_session.with_equipment_use(selected_equipment, time_used)

            material = equipment_frame.get_material()
            amount_consumed = int(equipment_frame.amount_used.get())

            eq_use_log.with_consumed_materials(material, amount_consumed)

    api_client.signout(sign_out_request)







