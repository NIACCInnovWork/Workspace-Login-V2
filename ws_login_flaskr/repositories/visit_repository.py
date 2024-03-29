from ws_login_domain import User, Visit
from ws_login_flaskr.repositories.matchpolicy import VisitMatchPolicy

from ws_login_flaskr.db import MySQLConnection

import datetime as dt
from typing import List


class VisitRepository:
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    def create_for(self, user: User, start_time: dt.datetime):
        """
        Method to create a new visit in the database. Static method so that it can be called independent of a specific
        object.  Calls out to the 'load' method after creating the visit in the database.

        :param user_id: Primary Key of the user who created this visit
        :param start_time: The time at which the visit started. (Generally This
            is the current time)
        :return: Visit object of the visit just added to the database
        """
        curr = self.conn.cursor()
        sql_create_command = "INSERT INTO visits (user_id, start_time) VALUES (%s, %s)"
        curr.execute(sql_create_command, (user.user_id, start_time))
        self.conn.commit()
        curr.close()
        return Visit(curr.lastrowid, user.user_id, start_time, None)

    def load_after_create(self, start_time: dt.datetime):
        """
        Method to load the visit from the database which was just added by the create method.  Because the database
        generates the visit_id and a user_id will be associated with multiple visits, this method uses the start_time
        timestamp as a unique identifier for loading in the visit record.

        :param start_time: Timestamp generated on the creation of the visit
        :return: Visit object with the timestamp requested
        """
        curr = self.conn.cursor()
        sql_load_command = "SELECT * FROM visits WHERE start_time = %s;"
        curr.execute(sql_load_command, (start_time,))
        record = curr.fetchone()
        print("Visit: ", record)
        # I suspect this will currently will throw an error because timestamp (record[3]) cannot be null
        return Visit(record[0], record[1], record[2], record[3])

    def load_all(self) -> List[Visit]:
        curr = self.conn.cursor()
        curr.execute("SELECT * FROM visits")
        rows = curr.fetchall()
        curr.close()

        # I suspect this will currently will throw an error because timestamp (record[3]) cannot be null

        return [Visit(row[0], row[1], row[2], row[3]) for row in rows] 

    def load_by_id(self, visit_id: int) -> List[Visit]:
        curr = self.conn.cursor()
        curr.execute("SELECT * FROM visits WHERE visit_id = %s", (visit_id,))
        row = curr.fetchone()
        curr.close()
        if not row:
            return None

        # I suspect this will currently will throw an error because timestamp (record[3]) cannot be null

        return Visit(row[0], row[1], row[2], row[3])

    def load_by_user(self, user: User, match: VisitMatchPolicy=VisitMatchPolicy.ALL()):
        """
        This method allows the loading of a particular visit by the user's name.

        :param user_name: Username of the visit to be loaded
        :return: Visit object with the timestamp requested
        """
        curr = self.conn.cursor()
        sql_load_command = f"SELECT * FROM visits WHERE user_id = %s {match.visits_sql}"
        
        curr.execute(sql_load_command, (user.user_id,))
        rows = curr.fetchall()
        curr.close()

        # I suspect this will currently will throw an error because timestamp (record[3]) cannot be null

        return [Visit(row[0], row[1], row[2], row[3]) for row in rows] 

    def update(self, visit: Visit):
        curr = self.conn.cursor()
        curr.execute(
            "UPDATE visits SET user_id=%s, start_time=%s, end_time=%s WHERE visit_id=%s", 
            (visit.user_id, visit.start_time, visit.end_time, visit.visit_id)
        )
        curr.close()


    def get_logged_in_users(self):
        """
        Class that queries the database for users which are currently logged in.

        :return: List of names of the members who have a visit with no logout timestamp
        """
        my_cursor = self.conn.cursor()
        sql_logged_in_users_command = "SELECT users.name, users.user_id FROM users JOIN visits ON " \
                                      "users.user_id = visits.user_id WHERE visits.end_time IS NULL"
        my_cursor.execute(sql_logged_in_users_command)
        logged_in_users = my_cursor.fetchall()

        return logged_in_users

    def check_logged_in(self, user_id: int):
        """
        Load the visit from the database with the given user_id and no end_time.
        
        :param user_id: Integer user_id foreign key for the visit.
        :return: None
        """
        my_cursor = self.conn.cursor()
        sql_logged_in_command = "SELECT * FROM visits WHERE user_id = %s AND end_time IS NULL"
        my_cursor.execute(sql_logged_in_command, (user_id,))
        record = my_cursor.fetchone()
        visit = Visit(record[0], record[1], record[2], record[3])

        return visit

    def sign_out_visit(self, visit_id: int):
        """
        Sign out from the visit database with the current time on sign-out.

        :param visit_id: Primary key of the visit to be updated.
        :return: None
        """
        my_cursor = self.conn.cursor()
        end_time = dt.datetime.now()
        sql_logged_out_command = "UPDATE visits SET end_time = %s WHERE visit_id = %s "
        my_cursor.execute(sql_logged_out_command, (end_time, visit_id))
        self.conn.commit()

