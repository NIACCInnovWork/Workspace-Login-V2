"""
NIACC Innovation Workspace Login V2
This file defines the 'Material' class.
Author: Anthony Riesen
"""

from ws_login_domain import Equipment

from dataclasses import dataclass
from typing import List

from ws_login_flaskr.db import MySQLConnection

@dataclass
class Material:
    material_id: int
    material_name: str
    unit: str

class MaterialRepository:
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    def get_material_for(self, equipment: Equipment) -> List[Material]:
        """
        Retrieve a list of all materials that can be used with a given machine.
        :param database: Database from which the data will be pulled
        :param equipment_id: ID of the equipment in question
        :return: List of material names
        """
        curr = self.conn.cursor()
        sql = "SELECT                                    " \
              "  mat.material_id,                        " \
              "  material_name,                          " \
              "  unit                                    " \
              "FROM materials AS mat                     " \
              "INNER JOIN equipment_materials AS em     " \
              "  ON em.material_id=mat.material_id " \
              "WHERE em.equipment_id = %s                "
        curr.execute(sql, (equipment.equipment_id,))
        return [Material(row[0], row[1], row[2]) for row in curr.fetchall()]
