"""
File to all plots for the Key Performance Indicator (KPI) report for the NIACC Innovation Workspace.
Author: Anthony Riesen
"""

from pathlib import Path
import tempfile
from dataclasses import dataclass

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams

from mysql.connector import MySQLConnection

@dataclass
class Figure:
    """ A figure / plot which can be included within a report

    This internally is stored as a png file on disk.
    """
    filepath: Path


def generate_total_report(database: MySQLConnection):
    """
    Generates all the plots to be included in the exported report for the Innovation Workspace
    :param database: Database from which the data are pulled.
    :return: None
    """
    # Loads in Data from Users and Visits Tables for Analysis
    df = load_all_visit_data(database)

    # Total Value Counts for general metrics
    # visits_per_user = df['user_id'].value_counts()  # Get the visit count for all users by id
    # visits_per_user_type = df['date_joined'].value_counts()  # Get the visit count per visit type
    #
    # Generate Plots
    # create_user_type_histogram(df)
    # create_user_type_pie_chart(df)
    # print("BREAK")
    # group_by_user_type_over_time(df)
    # plot_visits_over_time(df)
    create_visit_heat_map(df)


def create_user_type_histogram(df: pd.DataFrame) -> Figure:
    """
    Creates a histogram of user types

    :param df: Pandas dataframe containing all users within the system. The df MUST 
    contain the column of 'user_type'.
    :return: Figure containg path to the generated file
    """
    figure = Figure(Path(tempfile.gettempdir()) / 'User_Type_Histogram.png')

    plt.hist(df['user_type'])
    plt.ylabel('Number of Users')
    plt.xlabel('User Type')
    plt.title('Total Number of Users by Type')
    plt.savefig(figure.filepath, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return figure


def create_user_type_pie_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a Pie Chart that includes the percentages of different user types visiting the 
    space in total.

    :param df: Dataframe including user and visit data.
    :return: Saves figure, no return value
    """
    figure = Figure(Path(tempfile.gettempdir()) / 'User Type Pie Chart.png')

    df = df.groupby(df.user_type).user_type.count()

    plt.style.use('seaborn-v0_8-muted')
    plt.pie(df, labels=df.index, autopct='%.2f %%', explode=[.05] * len(df))
    plt.title('User Type Percentages for All Users')
    plt.savefig(figure.filepath, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    plt.show()

    return figure


def plot_users_over_type(min, max, df, title="", types=[]):
    """
    Generates subplots used in group_by_user_type_over_time function. Creates subplots 
    with a uniform scale.

    :param min: Minimum date value
    :param max: Maximum date value
    :param df:  Dataframe containing visit data
    :param title: Title for the subplot
    :param types: User Types to be included on the subplot
    :return: Subplots to be used in the figure, no returned value
    """
    # ToDo - Currently, this function breaks if a type is listed that is not included in the dataframe. Should be fixed.
    for type in types:
        grouped_data = df
        if type != "ALL":
            print("Filtering type ", type)
            grouped_data = grouped_data[df.user_type == type]

        print(grouped_data.columns)
        grouped_data = grouped_data.groupby(['Year/Month/Day'])['start_time'].count().reset_index()

        date_range = pd.date_range(name="Year/Month/Day", start=min, end=max)
        grouped_data = grouped_data.set_index("Year/Month/Day")

        grouped_data = grouped_data.reindex(date_range, fill_value=0)

        plt.title(title)
        plt.plot(grouped_data.index.values, grouped_data['start_time'])
        plt.ylabel('Visit Count')
        plt.ylim((0, 19))
        plt.xticks(rotation=25)


def group_by_user_type_over_time(df: pd.DataFrame):
    """
    Create multiplot figure of number of users in the workspace over time.
    :param df: Dataframe containing User and Visit Data
    :return: Saves Figure, no returned value
    """
    # Create new DataFrame with start_time and user_type only (Note: Start Time is never null)
    type_data_analyzed = pd.DataFrame({'start_time': df['start_time'],
                                       'end_time': df['end_time'],
                                       'user_type': df['user_type']})
    type_data_analyzed['total_time'] = df['end_time'] - df['start_time']
    # Add a new row that contains the week and year
    type_data_analyzed['Year/Month/Day'] = type_data_analyzed['start_time'].apply(lambda x: x.date())
    min_date = type_data_analyzed['Year/Month/Day'].min()
    max_date = type_data_analyzed['Year/Month/Day'].max()
    plt.figure(figsize=(7.5, 11))
    plt.subplot(4, 1, 1)
    plot_users_over_type(min_date, max_date, type_data_analyzed, "Total Visits", ["ALL"])
    plt.subplot(4, 1, 2)
    plot_users_over_type(min_date, max_date, type_data_analyzed, "Students / Staff", ["Student", "Staff"])
    plt.subplot(4, 1, 3)
    plot_users_over_type(min_date, max_date, type_data_analyzed, "Entrepreneur / Business Member", ["Entrepreneur"])
    plt.subplot(4, 1, 4)
    plot_users_over_type(min_date, max_date, type_data_analyzed, "Community Member", ["Community_Member"])
    plt.tight_layout()
    plt.savefig('plots/Users Over Time.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    # plt.show()


def create_visit_heat_map(df: pd.DataFrame) -> Figure:
    """
    Generates a heatmap plot of all visits within the space. This should provide a sense
    of when the space is most in demand.

    :param df: Dataframe containing User and Visit Data
    :return: Figure of the heatmap
    """
    figure = Figure(Path(tempfile.gettempdir()) / 'HeatMapData.png')
    
    # Range over which the heatmap is accumulated
    min_date = df.start_time.min()
    max_date = df.end_time.max()
    days = (max_date - min_date).days + 1

    # Build 2d matrix where row = hour and col = day.
    heat_map_historic = np.zeros((24, days))
    heat_map_day_of_week = np.zeros((24, 7))
    # IMPORTANT making the assumption that a visit never goes past midnight
    for index, row in df.iterrows():
        start_day = (row['start_time'] - min_date).days
        start_hour = row['start_time'].hour
        
        end_day = (row['end_time'] - min_date).days
        end_hour = row['end_time'].hour

        for hour in range(start_hour, end_hour + 1):
            heat_map_historic[hour][start_day] += 1
        
        for hour in range(start_hour, end_hour + 1):
            heat_map_day_of_week[hour][row['start_time'].day_of_week] += 1

    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))
    fig.tight_layout(h_pad=8)
    ax_historic = axs[0]
    ax_day_of_week = axs[1]

    # Render heatmap Historic
    ax_historic.set_title("Heat map for visitors over day of the week")
    ax_historic.imshow(heat_map_historic, aspect='auto')
    ax_historic.set_title(f"Heat map of visitors present from {min_date.date()} to {max_date.date()}")
    ax_historic.set_xticks(
            np.arange(days), 
            labels=[ min_date.date() + pd.Timedelta(days=day) if day % 2 == 0 else "" for day in range(days) ], 
            rotation = 90
    )
    ax_historic.set_yticks(np.arange(24), labels=[
        '12 AM', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
        '12 PM', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'
    ])
    
    # Render heatmap day of week
    ax_day_of_week.imshow(heat_map_day_of_week, aspect='auto')
    ax_day_of_week.set_title(f"Heat map of visitors present from {min_date.date()} to {max_date.date()}")
    ax_day_of_week.set_xticks(
            np.arange(7), 
            labels=[ 'SUN', 'MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT' ], 
            rotation = 90
    )
    ax_day_of_week.set_yticks(np.arange(24), labels=[
        '12 AM', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
        '12 PM', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'
    ])

    fig.savefig(figure.filepath, dpi=300, pad_inches=0.25)
    return figure 


def load_all_visit_data(database: MySQLConnection):
    """
    Load in the user and visit data
    :param database: Database from which the data are pulled.
    :return: Python Pandas Dataframe with data.
    """
    my_cursor = database.cursor()
    sql_load_command = "SELECT * FROM users " \
                       "INNER JOIN visits ON users.user_id = visits.user_id "
    my_cursor.execute(sql_load_command)
    df = pd.DataFrame(my_cursor.fetchall())
    df.drop(df.columns[[0]], axis=1, inplace=True)
    df.set_axis(["date_joined", "name", "user_type", "visit_id", "user_id", "start_time", "end_time"],
                axis=1, inplace=True)
    return df
