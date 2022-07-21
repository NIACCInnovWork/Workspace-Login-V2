"""
NIACC Innovation Workspace Login V2
This file initializes the workspace database and data structure.
Author: Anthony Riesen
"""

import mysql.connector
from config import database_password


def create_workspace_database():
    """
    Connects to MySQL and creates a new database if one doesn't already exist.
    :return: none.
    """
    mydb = mysql.connector.connect(
        host="localhost",  # Location of Database
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
        host="localhost",  # Location of Database
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
                      "user_id INTEGER, FOREIGN KEY(user_id) REFERENCES Users(user_id), "
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
                      "project_name VARCHAR(255) UNIQUE,"
                      "project_description VARCHAR(510),"
                      "project_type ENUM('Personal', 'Class', 'Entrepreneurial', 'Business')"
                      ")")


def create_visits_projects_table(database):
    """
    Create the 'visits_projects' table in the database if it does not already exist.
    This table is an intermediary table allowing a many-to-many relationship between the 'visits' table and the
    'projects' table reflecting the fact that some visits include multiple projects and some projects take multiple
    visits to complete.
    :param database: Database in which to add the table
    :return: none.
    """
    my_cursor = database.cursor()
    my_cursor.execute("CREATE TABLE IF NOT EXISTS visits_projects ("
                      "visit_project_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                      "visit_id INTEGER, FOREIGN KEY(visit_id) REFERENCES Visits(visit_id),"
                      "project_id INTEGER, FOREIGN KEY(project_id) REFERENCES Projects(project_id)"
                      ")")
