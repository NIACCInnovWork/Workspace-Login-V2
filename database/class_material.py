"""
NIACC Innovation Workspace Login V2
This file defines the 'Material' class.
Author: Anthony Riesen
"""

import mysql.connector


class Material:

    def __init__(self, material_id: int, material_name: str, unit: str):
        """
        Constructor for the Material object which matches the Material Table data structure
        :param material_id: Primary key of the table
        :param material_name: Name of the material
        :param unit: Unit of measurement of the material
        """
        self.material_id = material_id
        self.material_name = material_name
        self.unit = unit

    @staticmethod
    def get_material_names_for_equipment(database: mysql.connector, equipment_id: int):
        """
        Retrieve a list of all materials that can be used with a given machine.
        :param database: Database from which the data will be pulled
        :param equipment_id: ID of the equipment in question
        :return: List of material names
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT materials.material_name, materials.material_id " \
                           "FROM equipment " \
                           "INNER JOIN equipment_materials ON equipment.equipment_id=equipment_materials.equipment_id " \
                           "INNER JOIN materials ON equipment_materials.material_id=materials.material_id " \
                           "WHERE equipment.equipment_id = %s"
        my_cursor.execute(sql_load_command, (equipment_id,))
        records = my_cursor.fetchall()
        material_names = []
        for record in records:
            material_names.append((record[0],record[1]))

        return material_names

    @staticmethod
    def get_unit(database: mysql.connector, material_name: str):
        """
        Retrieve the unit associated with a particular material.
        :param database: Database from which the data will be pulled
        :param material_name: Name of the material in question
        :return: Unit of the material (String)
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT unit FROM materials WHERE material_name = %s"
        my_cursor.execute(sql_load_command, (material_name,))
        return my_cursor.fetchone()
