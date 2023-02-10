"""
NIACC Innovation Workspace Login V2
This file defines the 'Equipment' class.
Author: Anthony Riesen
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Equipment:
    equipment_id: int
    equipment_name: str

