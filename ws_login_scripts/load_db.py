
""" Utility for loading a database dump file into the database in kubernetes

Everything here operates in the default namespace.

The utility is run with the command:
>>> python -m ws_login_scripts.load_db

"""
from mysql.connector.connection import MySQLConnection
import os
from pathlib import Path
from ws_login_scripts.utils import KubeCtl, values_set_check, continue_prompt, exit_with
from ws_login_scripts.utils.prompts import continue_prompt 


def drop_all_tables(conn: MySQLConnection):
    try:
        cur = conn.cursor()

        # Fetch list of tables
        cur.execute("SHOW TABLES")
        tables = ', '.join(map(lambda x: x[0], cur.fetchall()))
        if not tables:
            return

        # Delete all tables
        cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cur.execute("DROP TABLES " + tables)
    finally:
        cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cur.close()


def load_from_file(conn: MySQLConnection, file):
    cur = conn.cursor()
    with open(file) as f:
        for sql_statement in f.read().split(';'):
            cur.execute(sql_statement)
    cur.close()
    conn.commit()

def run_utility():
    service_arg = os.environ.get("DB_SERVICE")
    secret_arg = os.environ.get("DB_SECRET")
    import_file_arg = os.environ.get("DB_IMPORT_FILE")

    print(
        "This utility will attempt to delete ALL existing data in the "
        "database and load in the data from the specified file. This utility "
        "DOES NOT create backups before proceeding."
    )
    print("")
    print("DB_SERVICE: " + str(service_arg))
    print("DB_SECRET: " + str(secret_arg))
    print("DB_IMPORT_FILE: " + str(import_file_arg))
    print("")

    values_set_check(service_arg, secret_arg, import_file_arg)
    continue_prompt("Are you sure you want to proceed?")

    path = Path(import_file_arg)
    if not path.exists() or not path.is_file():
        exit_with(f"'{path}' Does not exist.")


    kubectl = KubeCtl()
    db_secrets = kubectl.fetch_secrets(secret_arg)

    print("Opening portforward session")
    session = kubectl.port_forward(service_arg, 3306)
    try:

        conn = MySQLConnection(
                host=os.environ.get("DB_HOST", "127.0.0.1"),    # Location of Database
                user=os.environ.get("DB_USER", "root"),         # Database User
                passwd=db_secrets.get_secret("mysql-root-password"), # Database Password 
                database="workspace_login_data",
                charset="latin1",
            )
        
        drop_all_tables(conn)
        load_from_file(conn, import_file_arg)

        conn.close()
    finally:
        print("Closing Session")
        session.close()

if __name__ == '__main__':
    run_utility()
