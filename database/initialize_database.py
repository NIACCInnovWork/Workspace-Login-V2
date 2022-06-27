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


# def create_visits_table(database):
#     my_cursor = database.cursor()
#     my_cursor.execute("CREATE TABLE visits (visit_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
#                       "user_id INTEGER FOREIGN KEY, "
#                       "arrival_datetime DATETIME, "
#                       "departure_datetime DATETIME)")
#     my_cursor.execute()


# def create_projects_table(database):
#     my_cursor = database.cursor()
#     my_cursor.execute("CREATE TABLE projects (project_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
#                       "visit_id INTEGER FOREIGN KEY)")

    # my_cursor.execute("CREATE TABLE users (name VARCHAR(255), "
    #                   "email VARCHAR(255), "
    #                   "age INTEGER(10), "
    #                   "user_id INTEGER AUTO_INCREMENT PRIMARY KEY)")

    # sqlStuff = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    # record1 = ("John", "john@codemy.com", 40)

    # my_cursor.execute(sqlStuff, record1)
    # mydb.commit()

