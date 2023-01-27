"""
NIACC Innovation Workspace Login V2
This file defines the 'Material Consumption' class.
Author: Anthony Riesen
"""

import mysql.connector


class MaterialConsumed:

    def __init__(self, material_consumed_id: int, equipment_material_id: int, usage_log_id: int, amount_consumed: int):
        """
        Constructor for the MaterialConsumed object.
        :param material_consumed_id: Primary key for the material consumed record
        :param equipment_material_id: Foreign key from the join table of equipment and materials
        :param usage_log_id: Foreign key from the usage log
        :param amount_consumed: Amount of the material consumed
        """
        self.material_consumed_id = material_consumed_id
        self.equipment_material_id = equipment_material_id
        self.usage_log_id = usage_log_id
        self.amount_consumed = amount_consumed

    @staticmethod
    def factory(equipment_material_id: int, amount_consumed: int):
        """
        Method to partially construct the MaterialConsumed object without needing the material_consumed_id or
        usage_log_id
        :param equipment_material_id: Foreign key from the join table of equipment and materials
        :param amount_consumed: Amount of the material consumed
        :return: Partially constructed Material Consumed Object
        """
        print("Error in input to class_material_consumed factory")
        print(equipment_material_id)
        material_consumed = MaterialConsumed(0, equipment_material_id, 0, amount_consumed)

        return material_consumed

    @staticmethod
    def create(database: mysql.connector,  amount_consumed: int, equipment_material_id: int, usage_log_id: int):
        """
        Commit the material consumed object to the database with all data.
        :param database: Database into which the Innovation Workspace data is to be stored.
        :param amount_consumed: Amount of the material being consumed.
        :param equipment_material_id: Foreign key identifying both the equipment and material used.
        :param usage_log_id: Foreign key identifying the usage log record (and time) associated with this material
        consumption record.
        :return: Material Consumed Object commit to the database with all relevant data.
        """
        my_cursor = database.cursor()
        sql_create_command = "INSERT INTO materials_consumed (equipment_material_id, usage_log_id, amount_consumed) " \
                             "VALUES (%s, %s, %s)"
        select_data = (equipment_material_id, usage_log_id, amount_consumed)
        my_cursor.execute(sql_create_command, select_data)

        return MaterialConsumed.load_last(database)

    @staticmethod
    def load_last(database: mysql.connector):
        """
        Loads the last entry in the material consumed table of the database.  This method should be replaced as there
        should be a way to pull the ID of the item during the create method.
        @ToDo - Update the Create method to return the primary key and remove this method.
        :param database: Innovation Workspace Database from which the data is pulled.
        :return: Material Consumed Object commit to the database with all relevant data.
        """
        my_cursor = database.cursor()
        sql_load_command = "SELECT * FROM materials_consumed ORDER BY materials_consumed_id DESC LIMIT 1"
        my_cursor.execute(sql_load_command)
        record = my_cursor.fetchone()

        material_consumed = MaterialConsumed(record[3], record[0], record[1], record[2])
        # Order adjusted for optional constructors...

        return material_consumed
