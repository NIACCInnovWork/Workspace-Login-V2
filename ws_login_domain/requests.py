import datetime as dt

from typing import List, Dict, Optional, Union
from ws_login_domain import Visit, ProjectType, Project, Equipment, Material

class SignoutRequest:
    def __init__(
            self, 
            visit_id: int,
            np_worksession: List['NewProjectWorkSession'], 
            ep_worksession: List['ExistingProjectWorkSession'],
            signout_time: Optional[dt.datetime] = None,
    ) -> None:
        """ Please use the "for_visit" factory function.
        """
        self.visit_id = visit_id
        self.np_worksession = np_worksession
        self.ep_worksession = ep_worksession
        self.signout_time = signout_time
   
    @staticmethod
    def for_visit(visit: Visit, signout_time: Optional[dt.datetime] = None) -> 'SignoutRequest':
        return SignoutRequest(visit.visit_id, [], [], signout_time)

    @staticmethod
    def from_dict(visit_id: int, req: Dict) -> 'SignoutRequest':
        np_ws = [ 
             NewProjectWorkSession.from_dict(x) 
             for x in req.get('newProjectWorkSessions', []) 
        ]

        ep_ws = [ 
            ExistingProjectWorkSession.from_dict(x) 
            for x in req.get('existingProjectWorkSessions', []) 
        ]
        signout_time = dt.datetime.fromisoformat(req['signoutTime']) if req.get('signoutTime') else None
            
        return SignoutRequest(visit_id, np_ws, ep_ws, signout_time)

    def to_dict(self):
        d = {
                "newProjectWorkSessions": [ x.to_dict() for x in self.np_worksession ],
                "existingProjectWorkSessions": [ x.to_dict() for x in self.ep_worksession ],
        }
        if self.signout_time:
            d['signoutTime'] = self.signout_time.isoformat()
        return d

    def __contains__(self, ws: Union['NewProjectWorkSession', 'ExistingProjectWorkSession']):
        return ws in self.np_worksession or ws in self.ep_worksession

    def with_new_project(self, name: str, description: str, type: ProjectType) -> 'NewProjectWorkSession':
        session = NewProjectWorkSession(NewProjectReq(name, description, type), [])
        self.np_worksession.append(session)
        return session

    def with_existing_project(self, project: Project) -> 'ExistingProjectWorkSession':
        session = ExistingProjectWorkSession(project.project_id, [])
        self.ep_worksession.append(session)
        return session

class NewProjectReq:
    """ Request to create a project which does not yet exist!!

    This class is a request to create a new project rather than representing a project which already exists.  As such, it has no ID field.
    """
    def __init__(self, name: str, description: str, type: ProjectType):
        self.name = name
        self.description = description
        self.type = type

    @staticmethod
    def from_dict(req):
        return NewProjectReq(req['name'], req['description'], ProjectType[req['type']])

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type.name
        }

    
class NewProjectWorkSession:
    def __init__(self, project: NewProjectReq, equipment_use_log: List['EquipmentUseLog']) -> None:
        self.project = project
        self.equipment_use_log = equipment_use_log
    
    @staticmethod
    def from_dict(req: Dict):
        return NewProjectWorkSession(
            NewProjectReq.from_dict(req['project']),
            [ 
                 EquipmentUseLog.from_dict(x) 
                 for x in req.get('equipmentUseLog', []) 
            ]
        )

    def to_dict(self) -> Dict:
        return {
            "project": self.project.to_dict(),
            "equipmentUseLog": [ entry.to_dict() for entry in self.equipment_use_log ],
        }

    def with_equipment_use(self, equipment: Equipment, time_used: dt.timedelta) -> 'EquipmentUseLog':
        log = EquipmentUseLog(equipment.equipment_id, time_used, [])
        self.equipment_use_log.append(log)
        return log



class ExistingProjectWorkSession:
    def __init__(self, project_id: int, equipment_use_log: List['EquipmentUseLog']):
        self.project_id = project_id
        self.equipment_use_log = equipment_use_log

    @staticmethod
    def from_dict(req: Dict):
        return ExistingProjectWorkSession(
            req["projectId"], 
            [ 
                 EquipmentUseLog.from_dict(x) 
                 for x in req.get('equipmentUseLog', []) 
            ]
        )

    def to_dict(self) -> Dict:
        return {
            "projectId": self.project_id,
            "equipmentUseLog": [ entry.to_dict() for entry in self.equipment_use_log ],
        }

    def with_equipment_use(self, equipment: Equipment, time_used: dt.timedelta) -> 'EquipmentUseLog':
        log = EquipmentUseLog(equipment.equipment_id, time_used, [])
        self.equipment_use_log.append(log)
        return log

class EquipmentUseLog:
    def __init__(
            self, 
            equipment_id: int, 
            time_used: dt.timedelta, 
            consumed_material: List['ConsumedMaterial']
    ):
        self.equipment_id = equipment_id
        self.time_used = time_used
        self.consumed_material = consumed_material

    @staticmethod
    def from_dict(req) -> 'EquipmentUseLog':
        return EquipmentUseLog(
            req["equipmentId"],
            dt.timedelta(seconds=req["timeUsed"]),
            [ 
                ConsumedMaterial.from_dict(x) 
                for x in req.get("consumedMaterial", []) 
             ]
        )

    def to_dict(self) -> Dict:
        return {
            "equipmentId": self.equipment_id,
            "timeUsed": self.time_used.seconds,
            "consumedMaterial": [ cm.to_dict() for cm in self.consumed_material ]
        }

    def with_consumed_materials(self, material: Material, quantity: int):
        self.consumed_material.append(ConsumedMaterial(
            material.material_id, 
            quantity, 
            "foobar"
        ))

class ConsumedMaterial:
    def __init__(self, material_id: int, quantity: int, units: str):
        self.material_id = material_id
        self.quantity = quantity
        self.units = units  # property isn't used

    @staticmethod
    def from_dict(req) -> 'ConsumedMaterial':
        return ConsumedMaterial(
                req['materialId'],
                req['quantity'],
                req['units'],   # property isn't used
        )

    def to_dict(self) -> Dict:
        return {
            "materialId": self.material_id,
            "quantity": self.quantity,
            "units": self.units, # property isn't used
        }
