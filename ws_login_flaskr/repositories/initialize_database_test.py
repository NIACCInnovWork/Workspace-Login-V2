# Unit tests to ensure the database is running correctly
"""
NIACC Innovation Workspace Login V2
Integration test file that tests that the database has been successfully created and all the necessary tables are
present.
Author: Anthony Riesen
"""
import unittest
from database.initialize_database import *


class TestDatabase(unittest.TestCase):

    # Checks to make sure MySQL is installed and running
    def test_sql_is_running(self):
        """
        Connects to MySQL on the machine to determine if it is running properly
        :return: test success or failure
        """
        mydb = mysql.connector.connect(
            host="localhost",  # Location of Database
            user="root",  # Database User
            passwd=database_password(),  # Database Password saved in config file (not on git)
        )
        # If the database exists, return "success" otherwise return "failure"
        if mydb is not None:
            is_running = "success"
        else:
            is_running = "failure"

        self.assertEqual(is_running, "success", "Something is wrong with the database.")

    # Check to see if Workspace Database is running
    def test_workspace_database(self):
        """
        Connects to MySQL and determines whether the Workspace Login Data database is present
        :return: test success or failure
        """
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=database_password(),
        )
        my_cursor = mydb.cursor()
        my_cursor.execute("SHOW DATABASES")

        # Iterate to create clean database list
        database_list = []
        for db in my_cursor:
            database_list.append(str(db[0]))

        self.assertTrue('workspace_login_data' in database_list, "The proper database cannot be found.")

    def test_database_tables(self):
        """
        Retrieves tables in the Workspace Login Data database and checks whether they match the tables that should be
        present
        :return: test success or failure
        @todo Add Visits, Projects, and Equipment tables to the database and the tests.
        """
        database = start_workspace_database()
        my_cursor = database.cursor()
        my_cursor.execute("SHOW TABLES")

        # Iterate to create clean tables list
        table_list = []
        intended_tables_list = ['users', 'visits', 'projects', 'visits_projects']
        for table in my_cursor:
            table_list.append(str(table[0]))

        self.assertTrue(table_list == intended_tables_list, "Some tables are missing or extra tables exist.")


if __name__ == '__main__':
    unittest.main()
