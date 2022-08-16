"""
NIACC Innovation Workspace Login V2
This file defines the 'Equipment' class.
Author: Anthony Riesen
"""

import mysql.connector


class Equipment:

    def __init__(self, equipment_id: int, equipment_name: str):
        """
        Constructor for the Equipment class.
        :param equipment_id:  Primary Key of the equipment table.
        :param equipment_name: Name of the equipment.
        """
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name

    @staticmethod
    def get_all_equipment_names(database: mysql.connector):
        """
        This class gets all equipment names from the database for the purpose of populating the user interface.
        :param database: Database from which the names are pulled.
        :return: List of the names of the equipment.
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT equipment_name, equipment_id FROM equipment"
        my_cursor.execute(sql_load_command)
        records = my_cursor.fetchall()
        equipment_names = []
        for record in records:
            equipment_names.append((record[0], record[1]))

        return equipment_names
