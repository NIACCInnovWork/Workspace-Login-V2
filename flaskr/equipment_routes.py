import flask
from flask import Blueprint, abort
from flaskr.db import get_db
from database.class_equipment import EquipmentRepository
from database.class_material import Material, MaterialRepository
from typing import List, Dict

bp = Blueprint('equipment', __name__, url_prefix = '/api/equipment')

@bp.get('')
def get_all_equiptment() -> List[Dict]:
    equipment_repo = EquipmentRepository(get_db())

    return [
        {
            "id": eq.equipment_id,
            "name": eq.equipment_name,
            "ref": f"{flask.request.host_url}api/equipment/{eq.equipment_id}"
        }
        for eq in equipment_repo.get_all_equipment_names()
    ]


@bp.get('/<equipment_id>')
def get_equiptment_by_id(equipment_id: int) -> Dict:
    equipment_repo = EquipmentRepository(get_db())
    eq = equipment_repo.get_equipment(equipment_id)
    if eq is None:
        return flask.abort(404)

    return {
        "id": eq.equipment_id,
        "name": eq.equipment_name,
        "matRef": f"{flask.request.host_url}api/equipment/{eq.equipment_id}/materials"
    }


@bp.get('/<equipment_id>/materials')
def get_materials_for(equipment_id: int) -> List[Dict]:
    equiptment_repo = EquipmentRepository(get_db())
    material_repo = MaterialRepository(get_db())
    
    equipment = equiptment_repo.get_equipment(equipment_id)
    return [
        {
            "id": mat.material_id,
            "name": mat.material_name,
            "unit": mat.unit
        }
        for mat in material_repo.get_material_for(equipment)
    ]
