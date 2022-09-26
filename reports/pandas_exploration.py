"""
NIACC Innovation Workspace Login V2
This file begins the exploration into using Pandas to analyze data from the mySQL database backing this application.
Author: Anthony Riesen
"""

import pandas as pd
import mysql.connector


def run_report(database: mysql.connector):
    # practice_code(database)
    database_dataframe = load_entire_database(database)
    print(database_dataframe.shape)
    print()
    print(database_dataframe.head(15))
    print()
    print(database_dataframe['date_joined'].head(15))
    print()
    print(database_dataframe['date_joined'].median())
    print()
    print(database_dataframe.describe())  # Gives standard set of stats, but doesn't make sense to do with ids.
    print()
    print(database_dataframe.loc[0, 'date_joined'].day_name())
    print()
    print(database_dataframe['start_time'].dt.day_name())
    print()
    print(database_dataframe['start_time'].min())
    print(database_dataframe['start_time'].max())
    print(database_dataframe['start_time'].max() - database_dataframe['start_time'].min())
    # Find the time of a visit, possibly set as a new column
    print(database_dataframe['end_time'] - database_dataframe['start_time'])
    # Filtering data by Month & Year
    filter_month = (database_dataframe['end_time'] >= 'Sep 2022')
    filter_month2 = ((database_dataframe['end_time'] >= pd.to_datetime('2022-08-01')) &
                     (database_dataframe['end_time'] < pd.to_datetime('2022-09-01')))
    print(database_dataframe.loc[filter_month])
    print(database_dataframe.loc[filter_month2])



def load_entire_database(database):
    my_cursor = database.cursor()
    sql_load_command = "SELECT * FROM users " \
                       "INNER JOIN visits ON users.user_id = visits.user_id " \
                       # "INNER JOIN visits_projects ON visits_projects.visit_id = visits.visit_id " \
                       # "INNER JOIN projects ON visits_projects.project_id = projects.project_id " \
                       # "INNER JOIN usage_log ON usage_log.visit_project_id = visits_projects.visit_project_id " \
                       # "INNER JOIN materials_consumed ON materials_consumed.usage_log_id = usage_log.usage_log_id " \
                       # "INNER JOIN equipment_materials ON " \
                       # "equipment_materials.equipment_material_id = materials_consumed.equipment_material_id " \
                       # "INNER JOIN materials ON equipment_materials.material_id = materials.material_id " \
                       # "INNER JOIN equipment ON equipment_materials.equipment_id = equipment.equipment_id"
    my_cursor.execute(sql_load_command)
    df = pd.DataFrame(my_cursor.fetchall())
    df.set_axis(["user_id", "date_joined", "name", "user_type",
                 "visit_id", "user_id", "start_time", "end_time",
                 # "visit_project_id", "visit_id", "project_id",
                 # "project_id", "project_name", "project_description", "project_type",
                 # "usage_log_id", "visits_projects_id", "time_used",
                 # "materials_consumed_id", "equipment_material_id", "usage_log_id", "amount_consumed",
                 # "equipment_material_id", "equipment_id", "material_id",
                 # "material_id", "material_name", "unit",
                 # "equipment_id", "equipment_name"
                 ],
                axis=1, inplace=True)
    return df


def load_table_data(database: mysql.connector, table: str):
    my_cursor = database.cursor()
    sql_load_command = "SELECT * FROM " + table
    # note: I know this is very unsafe, but it is a quick workaround that works for now
    my_cursor.execute(sql_load_command)
    dataframe = pd.DataFrame(my_cursor.fetchall())
    header_list = load_table_headers(database, table)
    dataframe.set_axis(header_list, axis=1, inplace=True)
    # dataframe.set_index(header_list[1]) -- Doesn't seem to change anything here
    return dataframe


def load_table_headers(database: mysql.connector, table: str):
    my_cursor = database.cursor()
    sql_load_headers = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                       "WHERE TABLE_SCHEMA = 'workspace_login_data' AND TABLE_NAME = %s"
    my_cursor.execute(sql_load_headers, (table,))
    records = my_cursor.fetchall()
    header_list = []
    for record in records:
        header_list.append(record[0])

    return header_list


def practice_code(database: mysql.connector):
    users_dataframe = load_table_data(database, 'users')
    load_table_headers(database, 'users')
    visits_dataframe = load_table_data(database, 'visits')
    projects_dataframe = load_table_data(database, 'projects')
    visits_projects_dataframe = load_table_data(database, 'visits_projects')
    print(users_dataframe.head())
    print("")
    print(users_dataframe[['user_id', 'name']])  # Specific Columns
    print("")
    print(users_dataframe.iloc[[0, 1]])  # Specific Rows
    print("")
    print(users_dataframe.iloc[[0, 1], [0, 2]])  # Specific Rows and Columns Indexes
    print("")
    print(users_dataframe.loc[[0, 1], ['user_id', 'name']])  # Specific Rows and Columns labels
    print("")
    print(users_dataframe.loc[0:4, ['user_id', 'name']])  # Example of slicing, note not wrapped in brackets
    print("")
    print(users_dataframe.loc[0:4, 'user_id':'name'])  # Example of slicing, note not wrapped in brackets
    print("")
    print(users_dataframe['user_type'].value_counts())  # Provides a count of the number of each value
    print()
    filt = (users_dataframe['user_type'] == 'Student')  # Filtering Variable
    print(users_dataframe.loc[filt, 'name'])  # Select only the student names
    print()  # Other Sorting: & means "AND" | means "OR"
    filt2 = (users_dataframe['user_type'] == 'Student') & (users_dataframe['user_id'] < 7)  # Filtering considitions
    print(users_dataframe.loc[filt2, 'name'])
    filt3 = (users_dataframe['user_type'] == 'Student') | (
                users_dataframe['user_type'] == 'Staff')  # Filtering considitions
    print(users_dataframe.loc[filt3, ['name', 'user_id', 'user_type']])
    print()
    print(users_dataframe.loc[~filt3, ['name', 'user_id',
                                       'user_type']])  # ~ should give us everything that does not meet this filter
    print()
    family_filter = users_dataframe['name'].str.contains('Riesen', na=False)  # name contains Riesen, null ignored
    print(users_dataframe.loc[family_filter, ['name', 'user_type']])
    # df.apply() -> applies a function to every item in a series (row, column, etc.)
    # df.applymap() -> applies a function to every item in a dataframe (every entry)
    print()
    users_dataframe[['first_name', 'last_name']] = users_dataframe['name'].str.split(' ',
                                                                                     expand=True)  # expand changes to columns instead of list
    print(users_dataframe.head())


