"""
NIACC Innovation Workspace Login V2
This file defines the 'Project' class and the associated 'Project_Type' enum.
Author: Anthony Riesen
"""
from enum import Enum

import mysql.connector


class ProjectType(Enum):
    """
    Enum that defines the possible project types.
    """
    Personal = 1
    Class = 2
    Entrepreneurial = 3
    Business = 4


class Project:
    """
    Class that defines the data structure of the 'Project' object
    """
    def __init__(self, project_id: int, project_name: str, project_description: str, project_type: ProjectType):
        self.project_id = project_id
        self.project_name = project_name
        self.project_description = project_description
        self.project_type = project_type

    def __str__(self):
        return f"Project: projectID: {self.project_id}, Name: {self.project_name}," \
               f"Project Description: {self.project_description}, Project Type: {self.project_type}"

    @staticmethod
    def create(database: mysql.connector, project_name: str, project_description: str, project_type: ProjectType):
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO projects (project_name, project_description, project_type) " \
                             "VALUES (%s, %s, %s)"
        select_data = (project_name, project_description, project_type)
        my_cursor.execute(sql_create_command, select_data)
        database.commit()

        return Project.load(database, project_name)

    @staticmethod
    def load(database: mysql.connector, project_name: str):
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM projects WHERE project_name = %s"
        my_cursor.execute(sql_load_command, (project_name,))
        record = my_cursor.fetchone()

        project = Project(record[0], record[1], record[2], ProjectType[record[3]])

        # print(project)
        return project
