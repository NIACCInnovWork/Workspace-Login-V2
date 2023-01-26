"""
NIACC Innovation Workspace Login V2
This file defines the 'User' class and the associate 'User_Type' enum.
Author: Anthony Riesen
"""

from enum import Enum
import datetime as dt
from typing import List
from dataclasses import dataclass
from database.matchpolicy import MatchPolicy
from flaskr.db import MySQLConnection

class UserType(Enum):
    """
    A user (visitor) will be one of several categories of users. This enum lists out these
    options
    """
    Student = 1
    Staff = 2
    Entrepreneur = 3
    Business_Member = 4
    Community_Member = 5

@dataclass
class User:
    """
    A User (visitor) is someone who comes to the makerspace in order to work on projects.

    A user has name and other identifying information, a type, and a date joined.
    """
    user_id: int
    date_joined: dt.datetime
    name: str
    user_type: UserType

@dataclass
class UserSummary:
    id: int
    name: str

class UserRepository:
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    def create(self, name: str, user_type: UserType):
        """
        Constructs a new user object from the supplied parameters and inserts it into the database

        :param name: Full name of the user being added
        :param user_type: Enum that defines the user's type
        :return: Newly constructed user
        """
        # Prepare Data for Database
        date_joined = dt.datetime.now()
        curr = self.conn.cursor()
        sql_create_command = "INSERT INTO users (date_joined, name, user_type) VALUES (%s, %s, %s)"
        curr.execute(sql_create_command, (date_joined, name, user_type.value))
        self.conn.commit()  # End of Transaction
        curr.close()

        return User(curr.lastrowid, date_joined, name, user_type)

    def update(self, user: User):
        curr = self.conn.cursor()
        curr.execute("UPDATE users SET name = %s, user_type = %s WHERE user_id = %s", (user.name, user.user_type.name, user.user_id))
        self.conn.commit()

    def load_by_name(self, name: str):
        """
        Method to load a user from the database. Static method so that it can be called 
        independent of a specific object.  Deprecated Method actively being removed.

        :param name: Full name of the user being loaded
        :return: User object with the full name requested
        """
        curr = self.conn.cursor()
        sql_load_command = "SELECT * FROM users WHERE name = %s"
        curr.execute(sql_load_command, (name,))
        record = curr.fetchone()

        user = User(record[0], record[1], record[2], UserType[record[3]])

        return user

    def load(self, user_id: int):
        """
        Method to load a user from the database by their user_id.  Designed to replace 
        load_by_name method above.

        :param user_id: Primary key for the user being loaded
        :return: User object with the user_id provided
        """
        my_cursor = self.conn.cursor()
        sql_load_command = "SELECT * FROM users WHERE user_id = %s"
        my_cursor.execute(sql_load_command, (user_id,))
        record = my_cursor.fetchone()
        if record is None:
            return None
        user = User(record[0], record[1], record[2], UserType[record[3]])

        return user

    def get_all_visitors(self, match: MatchPolicy = MatchPolicy.ALL()) -> List[UserSummary]:
        """
        Method to select all visitors from the database.
        :param database: Workspace Login Database from which the user is loaded
        :return: List of users and user_ids
        """
        my_cursor = self.conn.cursor()
        sql_load_names_command = f"SELECT users.user_id, users.name FROM users WHERE true {match.users_sql}"
        my_cursor.execute(sql_load_names_command)

        return [UserSummary(rec[0], rec[1]) for rec in my_cursor.fetchall()]


