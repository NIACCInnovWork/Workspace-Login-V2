"""
NIACC Innovation Workspace Login V2
This file defines the 'ProjectWithMaterials' class that allows the Project class to be extended to include a list of
associated materials.
Author: Anthony Riesen
"""
from database.class_material_consumed import MaterialConsumed
from database.class_material_consumed_with_time import MaterialConsumedWithTime
from database.class_project import Project


class ProjectWithMaterials:

    def __init__(self, project: Project, materials_used: []):
        """
        Initializer for the ProjectWithMaterials class, allowing the data structure to match the user interface
        structure.
        :param project: Project object that materials are being added to.
        :param materials_used: List of materials associated with a give project.
        """
        self.project = project
        self.materials_used = materials_used

    def add_material(self, equipment_material_id: int, amount_consumed: int, time_used: int):
        """
        Method to add a material to the list of associated materials with a particular project.
        :param equipment_material_id: Primary key of the table associating a particular equipment and material
        :param amount_consumed: Amount of this material used in this project
        :param time_used: Amount of time this piece of equipment was used in seconds.
        :return: None
        """
        print(equipment_material_id)
        material_consumed = MaterialConsumed.factory(equipment_material_id, amount_consumed)
        material_consumed_with_time = MaterialConsumedWithTime(material_consumed, time_used)
        self.materials_used.append(material_consumed_with_time)

