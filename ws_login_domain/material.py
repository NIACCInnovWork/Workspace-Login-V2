"""
NIACC Innovation Workspace Login V2
This file defines the 'Material' class.
Author: Anthony Riesen
"""

from dataclasses import dataclass

@dataclass
class Material:
    material_id: int
    material_name: str
    unit: str

