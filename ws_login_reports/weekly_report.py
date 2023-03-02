"""
File to generate a weekly report snapshot for the NIACC innovation Workspace.
Author: Anthony Riesen

Period: 1 week prior to Report Date.
Metrics to report:
- Total Unique Users in the Workspace
- Total Time in Workspace

Need: Need to pull data from both the users and visits tables.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector


def generate_weekly_report(database: mysql.connector):
    """
    Method to pull out data for the IW Snapshot Metrics Sheet
    :param database: Database from which the data are pulled.
    :return: None
    """
    df = load_past_week_data(database)
    visits_per_user = df['name'].value_counts()  # Get the visit count for all users
    total_time_per_visit = df['end_time'] - df['start_time']  # Get the total time for each visit
    print(visits_per_user)
    print("Unique Users: " + str(visits_per_user.count()))
    print(total_time_per_visit)


def load_past_week_data(database: mysql.connector):
    """
    Load in the user and visit data from the past 7 days
    :param database: Database from which the data are pulled.
    :return: Python Pandas Dataframe with data.
    """
    my_cursor = database.cursor()
    sql_load_command = "SELECT * FROM users " \
                       "INNER JOIN visits ON users.user_id = visits.user_id " \
                       "WHERE visits.end_time > DATE(NOW()) - INTERVAL 7 DAY"
    my_cursor.execute(sql_load_command)
    df = pd.DataFrame(my_cursor.fetchall())
    df.set_axis(["user_id", "date_joined", "name", "user_type", "visit_id", "user_id", "start_time", "end_time"],
                axis=1, inplace=True)
    return df
