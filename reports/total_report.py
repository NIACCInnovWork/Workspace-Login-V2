"""
File to all plots for the Key Performance Indicator (KPI) report for the NIACC Innovation Workspace.
Author: Anthony Riesen
"""

import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams
import mysql.connector

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


def generate_total_report(database: mysql.connector):
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
    group_by_user_type_over_time(df)
    # plot_visits_over_time(df)


def create_user_type_histogram(df: pd.DataFrame):
    """
    Creates a histogram of user types
    :param df:
    :return:
    """
    plt.hist(df['user_type'])
    plt.ylabel('Number of Users')
    plt.xlabel('User Type')
    plt.title('Total Number of Users by Type')
    plt.savefig('plots/User_Type_Histogram.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    plt.show()


def create_user_type_pie_chart(df: pd.DataFrame):
    """
    Creates a Pie Chart that includes the percentages of different user types visiting the space in total.
    :param df: Dataframe including user and visit data.
    :return: Saves figure, no return value
    """
    num_staff = df.loc[df['user_type'] == 'Staff'].count()[0]
    num_community = df.loc[df['user_type'] == 'Community_Member'].count()[0]
    num_student = df.loc[df['user_type'] == 'Student'].count()[0]
    num_entrepreneur = df.loc[df['user_type'] == 'Entrepreneur'].count()[0]
    num_business = df.loc[df['user_type'] == 'Business_Member'].count()[0]
    labels = ['Business', 'Entrepreneur', 'Student', 'Community', 'Staff']
    explode = (.05, .05, .05, .05, .05)
    # colors = ['#8A6621', '#F08B19', '#FEBE10', '#334332', '#003976']
    plt.style.use('seaborn-v0_8-muted')
    plt.pie([num_business, num_entrepreneur, num_student, num_community, num_staff], labels=labels, autopct='%.2f %%',
            explode=explode)
    plt.title('User Type Percentages for All Users')
    plt.savefig('plots/User Type Pie Chart.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    plt.show()


def plot_users_over_type(min, max, df, title="", types=[]):
    """
    Generates subplots used in group_by_user_type_over_time function. Creates subplots with a uniform scale.
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


def load_all_visit_data(database: mysql.connector):
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
