"""
NIACC Innovation Workspace Login V2
This file defines the 'User' class and the associate 'User_Type' enum.
Author: Anthony Riesen
"""

from enum import Enum
import datetime
import mysql.connector


class UserType(Enum):
    """
    Enum that defines the possible user types.
    """
    Student = 1
    Staff = 2
    Entrepreneur = 3
    Business_Member = 4
    Community_Member = 5


class User:
    """
    Class that defines the data structure of the 'User' object
    """
    def __init__(self, user_id: int, date_joined: datetime.datetime.timestamp, name: str, user_type: UserType):
        """
        Constructor for 'User' class
        :param user_id: Unique identifier for each user, generated by the database
        :param date_joined: Timestamp that records the date and time the user first logged in
        :param name: Full name of the user, uniqueness is enforced so clients can search by name
        :param user_type: Enum value that defines this user's type out of the available options
        """
        self.user_id = user_id
        self.date_joined = date_joined
        self.name = name
        self.user_type = user_type

    def __str__(self):
        """
        Overrides the Print() functionality for the user to more cleanly output the object to the terminal
        :return: printout to terminal
        """
        return f"User: userID: {self.user_id}, name: {self.name}, " \
               f"timeStamp: {self.date_joined}, userType: {self.user_type}"

    @staticmethod
    def create(database: mysql.connector, name: str, user_type: UserType):
        """
        Method to create a new user in the database.  Static method so that it can be called independent of a specific
        object. Calls out to the 'load' method after creating the user in the database.
        :param database: Workspace Login Database in which the user is added
        :param name: Full name of the user being added
        :param user_type: Enum that defines the user's type
        :return: User object of the user just added to the database
        """
        # Prepare Data for Database
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Create current timestamp
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO users (date_joined, name, user_type) VALUES (%s, %s, %s)"
        select_data = (timestamp, name, user_type.value)
        my_cursor.execute(sql_create_command, select_data)
        database.commit()  # End of Transaction

        return User.load(database, name)

    @staticmethod
    def load(database: mysql.connector, name: str):
        """
        Method to load a user from the database. Static method so that it can be called independent of a specific
        object.
        :param database: Workspace Login Database from which the user is loaded
        :param name: Full name of the user being loaded
        :return: User object with the full name requested
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM users WHERE name = %s"
        my_cursor.execute(sql_load_command, (name,))
        record = my_cursor.fetchone()

        user = User(record[0], record[1], record[2], UserType[record[3]])

        # print(user)
        return user

    @staticmethod
    def get_all_visitors(database: mysql.connector):
        """
        Method to select all visitors from the database
        :param database: Workspace Login Database from which the user is loaded
        :return: List of visitors
        """
        my_cursor = database.cursor()
        sql_load_names_command = "SELECT name FROM users"
        my_cursor.execute(sql_load_names_command)

        return my_cursor.fetchall()

