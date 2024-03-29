"""
NIACC Innovation Workspace Login V2
This file defines the 'Usage Log Entry' class.
Author: Anthony Riesen
"""

import mysql.connector


class UsageLogEntry:

    def __init__(self, usage_log_id: int, visit_project_id: int, time_used: int):
        """
        Constructor for the UsageLogEntry class and the corresponding records in the database table.
        :param usage_log_id: Primary key for the usage_log table.
        :param visit_project_id: Foreign key connecting this usage instance with a particular visit and project.
        :param time_used: Total time the piece of equipment was used in seconds.
        """
        self.usage_log_id = usage_log_id
        self.visit_project_id = visit_project_id
        self.time_used = time_used

    @staticmethod
    def create(
            database: mysql.connector, 
            visit_project_id: int, 
            time_used: int
    ):
        """
        Create an entry in the database's UsageLog table.
        @Todo - Investigate the "lastrow" method on a database connection cursor following an INSERT database command
        More Info: https://www.geeksforgeeks.org/get-the-id-after-insert-into-mysql-database-using-python/
        :param database: Workspace database into which the data is inserted.
        :param visit_project_id: Foreign key from the join table between visits and projects.
        :param time_used: Time a particular piece of equipment was used in seconds.
        :return: The UsageLogEntry object just created
        """
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO usage_log (visit_project_id, time_used) VALUES (%s, %s)"
        select_data = (visit_project_id, time_used)
        my_cursor.execute(sql_create_command, select_data)

        return UsageLogEntry.load(database, my_cursor.lastrowid)

    @staticmethod
    def load(database: mysql.connector, usage_log_id: int):
        """
        Method to load in a usage_log entry from the database.  Called in Create method.
        :param database: Innovation Workspace database in which the data is stored
        :param usage_log_id: Primary key for the usage_log in question
        :return: Usage_log object containing the details from the database
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM usage_log WHERE usage_log_id = %s"
        my_cursor.execute(sql_load_command, (usage_log_id,))
        record = my_cursor.fetchone()

        usage_log_entry = UsageLogEntry(record[0], record[1], record[2])

        return usage_log_entry

