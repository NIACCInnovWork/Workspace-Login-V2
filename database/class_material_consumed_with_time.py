"""
NIACC Innovation Workspace Login V2
This file defines the 'MaterialConsumedWithTime' class that allows the MaterialsConsumed class to be extended to
include the time used.
Author: Anthony Riesen
"""
from database.class_material_consumed import MaterialConsumed


class MaterialConsumedWithTime:

    def __init__(self, material_consumed: MaterialConsumed, time_used: int):
        """
        Constructor for the MaterialConsumedWithTime class. With allows time to be attached to the material.
        :param material_consumed: MaterialConsumed object to attach time used.
        :param time_used: Time the equipment was used in seconds.
        """
        self.material_consumed = material_consumed
        self.time_used = time_used
