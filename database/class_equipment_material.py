"""
NIACC Innovation Workspace Login V2
This file defines the 'EquipmentMaterial' class and associated methods.
Author: Anthony Riesen
"""

import mysql.connector


class EquipmentMaterial:

    def __init__(self, equipment_material_id, equipment_id, material_id):
        """
        Constructor for the Equipment_Material join table in the database
        :param equipment_material_id: Primary Key of the join table
        :param equipment_id: Foreign Key of the Equipment Table
        :param material_id: Foreign Key of the Material Table
        """
        self.equipment_material_id = equipment_material_id
        self.equipment_id = equipment_id
        self.material_id = material_id

    @staticmethod
    def get_equipment_material_id(database: mysql.connector, equipment_id: int, material_id: int):
        """
        Given an equipment and material id, return the primary key from the equipment_material join table.
        :param database: Innovation Workspace Database
        :param equipment_id: Foreign Key of the Equipment Table
        :param material_id: Foreign Key of the Material Table
        :return: Primary Key of the equipment_material join table
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT equipment_material_id FROM equipment_materials " \
                           "WHERE equipment_id = %s AND material_id = %s"
        my_cursor.execute(sql_load_command, (equipment_id, material_id,))
        record = my_cursor.fetchone()

        return record[0]
