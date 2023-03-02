from ws_login_domain import Project, ProjectSummary, ProjectType, User
from ws_login_flaskr.db import MySQLConnection

from typing import List

class ProjectRepository:
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    def create(self, name: str, description: str, project_type: ProjectType):
        """
        Method to create a new project in the database. Calls out to the 'load' method after 
        creating the user in the database.

        :param project_name: Unique name for the project @Todo - Perhaps remove unique qualifier
        :param project_description: Description of the project that includes additional details that help distinguish
        this particular project from any other
        :param project_type: num value that defines this project's type out of the available options
        :return: Project object of the projected just added to the database
        """
        my_cursor = self.conn.cursor()
        sql_create_command = """
            INSERT INTO projects
                (project_name, project_description, project_type) 
                VALUES (%s, %s, %s)
            """
        my_cursor.execute(sql_create_command, (name, description, project_type.value))
        self.conn.commit()

        return self.load(my_cursor.lastrowid)

    def load(self, project_id: int):
        """
        Method to load a user from the database. Static method so that it can be call independently of a specific
        object.

        :param database: Workspace Login Database from which the project is loaded
        :param project_id: Primary key for the project
        :return: Project object for record
        """
        my_cursor = self.conn.cursor()
        sql_load_command = "SELECT * FROM projects WHERE project_id = %s"
        my_cursor.execute(sql_load_command, (project_id,))
        record = my_cursor.fetchone()
        if not record:
            return None
        project = Project(record[0], record[1], record[2], ProjectType[record[3]])

        return project

    def load_for(self, user: User):
        """
        Fetches all projects with which the user is associated
        """
        curr = self.conn.cursor()
        sql = "SELECT DISTINCT projects.project_id, projects.project_name FROM visits_projects " \
                           "INNER JOIN visits ON visits_projects.visit_id=visits.visit_id " \
                           "INNER JOIN users ON visits.user_id=users.user_id " \
                           "INNER JOIN projects ON visits_projects.project_id=projects.project_id " \
                           "WHERE users.user_id=%s"
        curr.execute(sql, (user.user_id,))
        return [ ProjectSummary(row[0], row[1]) for row in curr.fetchall() ]

    def load_all_projects(self) -> List[ProjectSummary]:
        my_cursor = self.conn.cursor()
        sql_load_command = "SELECT project_id, project_name FROM projects"
        my_cursor.execute(sql_load_command)
        record_list = my_cursor.fetchall()
        
        return [ProjectSummary(rec[0], rec[1]) for rec in record_list]

