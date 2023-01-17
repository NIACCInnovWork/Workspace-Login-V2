"""
NIACC Innovation Workspace Login V2
This file initializes the workspace database and data structure.
Author: Anthony Riesen
"""

import mysql.connector
from config import database_host, database_password


def create_workspace_database():
    """
    Connects to MySQL and creates a new database if one doesn't already exist.
    :return: none.
    """
    mydb = mysql.connector.connect(
        host=database_host(),  # Location of Database
        user="root",  # Database User
        passwd=database_password()  # , Database Password saved in config file (not on git)
    )
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS workspace_login_data")


# Connect to Existing Database
def start_workspace_database():
    """
    Establishes connection to the workspace login database
    :return: database object
    """
    mydb = mysql.connector.connect(
        host=database_host(),  # Location of Database
        user="root",  # Database User
        passwd=database_password(),  # Database Password saved in config file (not on git)
        database="workspace_login_data"
    )
    return mydb


def create_users_table(database: mysql.connector):
    """
    Creates the 'users' table in the database if it does not already exist.
    :param database: database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                      "user_id INTEGER AUTO_INCREMENT PRIMARY KEY, "
                      "date_joined TIMESTAMP, "
                      "name VARCHAR(255) UNIQUE, "
                      "user_type ENUM('Student', 'Staff', 'Entrepreneur', 'Business_Member', 'Community_Member')"
                      ")")


def create_visits_table(database):
    """
    Create the 'visits' table in the database if it does not already exist.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS visits ("
                      "visit_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id), "
                      "start_time DATETIME, "
                      "end_time DATETIME"
                      ")")


def create_projects_table(database):
    """
    Create the 'projects' table in the database if it does not already exist.
    @Todo - Consider removing the UNIQUE qualifier on project_name, see todos in class_project as well.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS projects ("
                      "project_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "project_name VARCHAR(255),"
                      "project_description VARCHAR(510),"
                      "project_type ENUM('Personal', 'Class', 'Entrepreneurial', 'Business', 'Community', 'WorkStudy')"
                      ")")


def create_visits_projects_table(database):
    """
    Create the 'visits_projects' table in the database if it does not already exist.
    This table is an intermediary table allowing a many-to-many relationship between the 'visits' table and the
    'projects' table reflecting the fact that some visits include multiple projects and some projects take multiple
    visits to complete.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS visits_projects ("
                      "visit_project_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "visit_id INTEGER, FOREIGN KEY(visit_id) REFERENCES visits(visit_id),"
                      "project_id INTEGER, FOREIGN KEY(project_id) REFERENCES projects(project_id)"
                      ")")


def create_usage_log_table(database):
    """
    Create the 'usage log' table in the database if it does not already exist.
    This table primarily stores the time a piece of equipment was used and links the usage to the
    'materials_consumed_log'.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS usage_log ("
                      "usage_log_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "visit_project_id INTEGER, FOREIGN KEY(visit_project_id) "
                      "REFERENCES visits_projects(visit_project_id),"  # Continuation of visit_project_id
                      "time_used INTEGER"  # Length of time equipment was used stored in seconds
                      ")")


def create_equipment_table(database):
    """
    Create the 'equipment' table in the database if it does not already exist.
    This table primarily stores the name of each piece of available equipment the workspace owns allowing it to
    dynamically scale as the workspace grows.  Currently, this table is updated manually by makerspace staff via the
    MySQLWorkbench application.
    @ToDo - Consider: Should there be a 'retired' field for equipment that no longer is in use?
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS equipment ("
                      "equipment_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "equipment_name VARCHAR(255) UNIQUE"
                      ")")


def create_materials_table(database):
    """
    Create the 'materials' table in the database if it does not already exist.
    This table stores the materials used by workspace equipment along with the unit of measurement for these materials.
    Currently, this table is updated manually by makerspace staff via the MySQLWorkbench application.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS materials ("
                      "material_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "material_name VARCHAR(255),"  # With Color Information Included
                      "unit VARCHAR(255)"
                      ")")


def create_equipment_materials_table(database):
    """
    Create the 'equipment_materials' table in the database if it does not already exist.
    This table is an intermediary table allowing a many-to-many relationship between the 'equipment' table and the
    'materials' table reflecting the fact that some materials can be used across multiple machines and some machines can
    use multiple materials. Currently, this table is updated manually by makerspace staff via the MySQLWorkbench
    application.
    :param database: Database in which to add the table
    :return: none
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS equipment_materials ("
                      "equipment_material_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "equipment_id INTEGER, FOREIGN KEY(equipment_id) REFERENCES equipment(equipment_id),"
                      "material_id INTEGER, FOREIGN KEY(material_id) REFERENCES materials(material_id)"
                      ")")


def create_materials_consumed_table(database):

    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS materials_consumed ("
                      "materials_consumed_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "equipment_material_id INTEGER, FOREIGN KEY(equipment_material_id) "
                      "REFERENCES equipment_materials(equipment_material_id),"  # continuation of foreign key statement
                      "usage_log_id INTEGER, FOREIGN KEY(usage_log_id) REFERENCES usage_log(usage_log_id),"
                      "amount_consumed INTEGER"  
                      ")")
