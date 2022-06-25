from enum import Enum
import datetime
import mysql.connector


class UserType(Enum):

    Student = 1
    Staff = 2
    Entrepreneur = 3
    Business_Member = 4
    Community_Member = 5


class User:

    def __init__(self, user_id: int, date_joined: datetime.datetime.timestamp, name: str, user_type: UserType):
        self.user_id = user_id
        self.date_joined = date_joined
        self.name = name
        self.user_type = user_type

    def __str__(self):
        return f"User userID: {self.user_id}, name: {self.name},timeStamp: {self.date_joined}, userType: {self.user_type}"

    @staticmethod  # Allows us to call this method to be called without already having an object
    def create(database: mysql.connector, name: str, user_type: UserType):
        # Prepare Data for Database
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Create current timestamp
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO users (date_joined, name, user_type) VALUES (%s, %s, %s)"
        select_data = (timestamp, name, user_type)
        my_cursor.execute(sql_create_command, select_data)
        database.commit()  # End of Transaction

        return User.load(database, name)

    @staticmethod
    def load(database: mysql.connector, name: str):
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM users WHERE name = %s"
        my_cursor.execute(sql_load_command, (name,))
        record = my_cursor.fetchone()

        user = User(record[0], record[1], record[2], UserType[record[3]])

        print(user)
        return user

