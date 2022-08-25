"""
NIACC Innovation Workspace Login V2
This file defines a composite object used for constructing a completed logout transaction.  This class is intended to
be atomic, so it either all works and can be committed to the database or none of it reaches the database. This class
is used by the sign_out_controller file as it pulls data from the user interface and constructs this object.
Author: Anthony Riesen
"""
import tkinter.messagebox

import mysql.connector

from database.class_material_consumed import MaterialConsumed
from database.class_project import Project, ProjectType
from database.class_project_with_materials import ProjectWithMaterials
from database.class_usage_log_entry import UsageLogEntry
from database.class_visit import Visit
from database.class_visit_project import VisitProject


class SignOutComposite:

    def __init__(self, visit: Visit, project_list: []):
        """
        Constructor for the composite object that includes data from the UI used in signing out.
        :param visit: Visit object for the active visit being signed out
        :param project_list: List of Project with Materials objects used during this visit
        """
        self.visit = visit
        self.project_list = project_list

    @staticmethod
    def create(database: mysql.connector, user_name: str):
        """
        Create SignOutComposite object by pulling the visit object from the database and using it in the constructor
        to create the object.
        :param database: Innovation Workspace Database
        :param user_name: Name of the user to be logged out
        :return: Composite object to be used in signing out
        """
        # Step 1: Pull the visit data and create completed visit object
        visit = Visit.load_by_user_name(database, user_name)

        # Step 2: Create and Return SignOutComposite Object
        composite = SignOutComposite(visit, [])

        return composite

    def add_project(self, project_id: int, project_name: str, project_description: str, project_type: ProjectType,
                    database: mysql.connector):
        """
        Method to add projects to a SignOutComposite object.  This includes constructing the projects themselves and
        checking to make sure all the data is present.
        :param project_id: ID of the project, set to 0 if not yet in the database
        :param project_name: Name of the Project
        :param project_description: Description of the project for additional detail
        :param project_type: Classification of the project for simpler analysis
        :param database: Innovation Workspace Database used to load info if project already exists
        :return: None
        """

        # Create a new Project object to be stored later
        project = ""  # placeholder for project
        if project_id == 0:
            project = Project.factory(project_name, project_description, project_type)  # No project_id yet
        elif project_id != 0:
            project = Project.load(database, project_id)
        # tkinter.messagebox.showinfo("Project Created", "The project '" + project_name + "' has been created.")

        # Create ProjectWithMaterials instance and append to project list
        project_with_materials = ProjectWithMaterials(project, [])
        self.project_list.append(project_with_materials)  # Add the Project to the Project List

        return len(self.project_list)  # Returns the project length as the index of the last added project

    def add_material_usage(self, project_index, equipment_material_id, amount_consumed, time_used):
        """
        Method to add materials to the compound Project with Materials object
        :param project_index: Index of the Project to be added to in the project list
        :param equipment_material_id: Foreign Key of the equipment_material join table
        :param amount_consumed: Amount of the material consumed
        :param time_used: Amount of time the equipment was used
        :return: None
        """
        print(equipment_material_id)
        self.project_list[project_index].add_material(equipment_material_id, amount_consumed, time_used)

    def commit_data(self, database: mysql.connector):
        """
        Method to persist all data in the SignOutComposite object to the database
        :param database: Innovation Workspace Database to which the data will be committed
        :return: None, tkinter message box noting the data has been successfully committed
        """
        # Update the visit to have the current end time
        Visit.sign_out_visit(database, self.visit.visit_id)
        # Commit Projects to database and create visit_project table entry
        for project_with_materials in self.project_list:
            # Create Project in the database
            recorded_project = ""  # Placeholder for project
            if project_with_materials.project.project_id == 0:
                recorded_project = Project.create(database, project_with_materials.project.project_name,
                                                  project_with_materials.project.project_description,
                                                  project_with_materials.project.project_type)
            elif project_with_materials.project.project_id != 0:
                recorded_project = project_with_materials.project

            # Create VisitProject in the database to link the project with the visit
            visit_project = VisitProject.create(database, self.visit.visit_id, recorded_project.project_id)

            for material_consumed_with_time in project_with_materials.materials_used:
                # Create UsageLog in the database to record time and link with the materials consumed
                usage_log_entry = UsageLogEntry.create(database, visit_project.visit_project_id,
                                                       material_consumed_with_time.time_used)

                print(material_consumed_with_time.material_consumed.equipment_material_id)

                # Create MaterialConsumed in the database to record
                MaterialConsumed.create(database, material_consumed_with_time.material_consumed.amount_consumed,
                                        material_consumed_with_time.material_consumed.equipment_material_id,
                                        usage_log_entry.usage_log_id)

        tkinter.messagebox.showinfo("Data Committed Properly", "The data has been commit to the database.")
