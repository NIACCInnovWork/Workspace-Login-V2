"""
NIACC Innovation Workspace Login V2
This file defines the 'Equipment' class.
Author: Anthony Riesen
"""
from dataclasses import dataclass
from typing import List, Optional


from ws_login_flaskr.db import MySQLConnection

@dataclass
class Equipment:
    equipment_id: int
    equipment_name: str

class EquipmentRepository:
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    def get_all_equipment_names(self) -> List[Equipment]:
        """
        This class gets all equipment names from the database for the purpose of populating the user interface.
        :param database: Database from which the names are pulled.
        :return: List of the names of the equipment.
        """
        curr = self.conn.cursor()
        curr.execute("SELECT equipment_id, equipment_name FROM equipment")
        return [Equipment(rec[0], rec[1]) for rec in curr.fetchall()]

    def get_equipment(self, equipment_id) -> Optional[Equipment]:
        curr = self.conn.cursor()
        curr.execute("SELECT equipment_id, equipment_name FROM equipment WHERE equipment_id = %s", (equipment_id,))
        row = curr.fetchone()
        if row is None:
            return None
        return Equipment(row[0], row[1])
        

