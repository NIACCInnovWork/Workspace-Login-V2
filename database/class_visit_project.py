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
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO visits_projects (visit_id, project_id) VALUES (%s, %s)"
        select_data = (visit_id, project_id)
        my_cursor.execute(sql_create_command, select_data)
        database.commit()

        return VisitProject.load(database)

    @staticmethod
    def load(database: mysql.connector):
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM visits_projects ORDER BY visit_project_id DESC LIMIT 1"
        my_cursor.execute(sql_load_command)
        record = my_cursor.fetchone()

        visit_project = VisitProject(record[0], record[1], record[2])

        # print(visit_project)
        return visit_project

