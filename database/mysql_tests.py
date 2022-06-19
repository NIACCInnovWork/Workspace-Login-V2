import mysql.connector
from config import database_password


def start_sql_database():
    mydb = mysql.connector.connect(
        host="localhost",  # Location of Database
        user="root",  # Database User
        passwd=database_password(),  # Database Password saved in config file (not on git)
        database="testbd"
    )

    my_cursor = mydb.cursor()

    # my_cursor.execute("CREATE DATABASE testbd")

    # my_cursor.execute("SHOW DATABASES")
    # for db in my_cursor:
    #     print(db[0])

    # my_cursor.execute("CREATE TABLE users (name VARCHAR(255), "
    #                   "email VARCHAR(255), "
    #                   "age INTEGER(10), "
    #                   "user_id INTEGER AUTO_INCREMENT PRIMARY KEY)")

    # my_cursor.execute("SHOW TABLES")
    # for table in my_cursor:
    #     print(table[0])

    sqlStuff = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    record1 = ("John", "john@codemy.com", 40)

    my_cursor.execute(sqlStuff, record1)
    mydb.commit()

