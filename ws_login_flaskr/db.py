import os
from flask import g
from mysql.connector.connection import MySQLConnection


def get_db() -> MySQLConnection:
    """ Constructs or fetches a new db connection

    The db connection is fetched from within the flask request context. If the connection doesn't exist, one is created
    and stored.

    :return: New db session
    """
    if 'db' not in g:
        g.db = MySQLConnection(
            host=os.environ.get("DB_HOST", "127.0.0.1"),    # Location of Database
            user=os.environ.get("DB_USER", "root"),         # Database User
            passwd=os.environ.get("DB_PASSWORD", "foobar"), # Database Password 
            database="workspace_login_data",
            charset="latin1",
        )
    return g.db


def close_db(e=None):
    """ Closes the request associated DB connection if one exists

    This function MUST be registered with the flask app explicitly
    """
    db: MySQLConnection = g.pop('db', None)
    if db is not None:
        db.close()
