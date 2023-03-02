""" Utility for createing a db backup of a service

This utility depends on both KubeCtl AND mysql or maria db commandline 
utilities being installed.
"""

import os, time
import subprocess as sp

from pathlib import Path

from mysql.connector.utils import subprocess
from ws_login_scripts.utils import \
    KubeCtl, \
    values_set_check, \
    continue_prompt, \
    exit_with


def dump_db(password: str, file: str):
    cmd = [
        "mariadb-dump", 
        "--host=127.0.0.1", 
        "--user=root", 
        "--password=" + password,
        "workspace_login_data" # DB name
    ]

    print(f"Executing {str(cmd).replace(password, '***')} > " + file)
    with open(file, 'w') as f:
        result = sp.run(
            [
                "mariadb-dump", 
                "--host=127.0.0.1", 
                "--user=root", 
                "--password=" + password,
                "workspace_login_data" # DB name
            ],
            stdout=f
        )


def run_utility():
    service_arg = os.environ.get("DB_SERVICE")
    secret_arg = os.environ.get("DB_SECRET")
    export_file_location = os.environ.get("DB_EXPORT_LOCATION")

    print(
        "This utility will attempt execute the mysqldump / mariadbdump "
        "commnad in order to create a backup file.  This command requires "
        "that the dbdump utility is installed AND that kubectl is installed."
    )
    print("")
    print("DB_SERVICE: " + str(service_arg))
    print("DB_SECRET: " + str(secret_arg))
    print("DB_EXPORT_LOCATION: " + str(export_file_location))
    print("")

    # This may exit the program without warning
    values_set_check(service_arg, secret_arg, export_file_location)
    continue_prompt("Are you sure you want to proceed?") 

    # Check if export path exists
    path = Path(export_file_location)
    parent = path.parent
    if not parent.exists():
        continue_prompt("Export directory doesn't exist. Do you want to create it?")
        parent.mkdir(parents=True)
    elif parent.is_file():
        exit_with(f"'{parent}' is a file and cannot be a parent directory")

    if path.is_file():
        continue_prompt(f"'{path}' already exists.  Do you want to overwrite?")
 
    k = KubeCtl()

    pf_session = k.port_forward(service_arg, 3306)
    print()
    try:
        db_secrets = k.fetch_secrets(secret_arg)
        dump_db(
            db_secrets.get_secret("mysql-root-password").decode('UTF-8'), 
            export_file_location
        )

    finally:
        pf_session.close()


if __name__ == '__main__':
    run_utility()
