"""
NIACC Innovation Workspace Login V2
This file defines the 'VisitProject' class.
Author: Anthony Riesen
"""
import mysql.connector


class VisitProject:
    """
    Class that defines the data structure of the 'VisitProject' object linking the visit and project tables.
    """
    def __init__(self, visit_project_id: int, visit_id: int, project_id: int):
        self.visit_project_id = visit_project_id
        self.visit_id = visit_id
        self.project_id = project_id

    def __str__(self):
        return f"VisitProjectID: {self.visit_project_id}, VisitID: {self.visit_id}, ProjectID: {self.project_id}"

    @staticmethod
    def create(database: mysql.connector, visit_id, project_id):
        """
        Method to create a new visit_project in the database. Static method so that it can be called independently of a
        specific object.  Calls out to the 'load' method after creating the visit_project in the database.
        :param database: Workspace Login Database in which the visit_project is added
        :param visit_id: Foreign key of the visit id
        :param project_id: Foreign key of the project id
        :return: VisitProject object just added to the database
        """
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO visits_projects (visit_id, project_id) VALUES (%s, %s)"
        select_data = (visit_id, project_id)
        my_cursor.execute(sql_create_command, select_data)

        return VisitProject.load(database)

    @staticmethod
    def load(database: mysql.connector):
        """
        Method to load the last VisitProject object that was commit to the database.
        @Todo - This should be able to be merged into the create method by returning the primary key during SQL INSERT
        :param database: Workspace Login Database from which the visit_project is pulled
        :return: VisitProject object
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM visits_projects ORDER BY visit_project_id DESC LIMIT 1"
        my_cursor.execute(sql_load_command)
        record = my_cursor.fetchone()

        visit_project = VisitProject(record[0], record[1], record[2])

        # print(visit_project)
        return visit_project

