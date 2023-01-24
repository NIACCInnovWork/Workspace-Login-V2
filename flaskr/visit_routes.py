import flask
from flask import Blueprint, abort
from database.class_material_consumed import MaterialConsumed
from database.class_project import ProjectRepository, ProjectType
from database.class_usage_log_entry import UsageLogEntry

from flaskr.db import get_db
from database.class_visit import VisitRepository
from database.class_visit_project import VisitProject
from database.class_equipment_material import EquipmentMaterial

from typing import List, Dict
import datetime as dt

bp = Blueprint('visits', __name__, url_prefix = '/api/visits')

@bp.get('')
def get_visits():
    visit_repo = VisitRepository(get_db())
    return [
        {
            "id": visit.visit_id,
            "ref": f"{flask.request.host_url}api/visits/{visit.visit_id}",
            "userId": visit.user_id,
            "startTime": visit.start_time,
            "endTime": visit.end_time,
        }
        for visit in visit_repo.load_all()
    ]

@bp.get('<visit_id>')
def get_visit_by_id(visit_id: int):
    visit_repo = VisitRepository(get_db())
    visit = visit_repo.load_by_id(visit_id)
    if not visit:
        flask.abort(404)

    return {
        "id": visit.visit_id,
        "userId": visit.user_id,
        "userRef": f"{flask.request.host_url}api/users/{visit.user_id}",
        "startTime": visit.start_time,
        "endTime": visit.end_time,
    }

class SignoutRequest:
    def __init__(
            self, 
            np_worksession: List['NewProjectWorkSession'], 
            ep_worksession: List['ExistingProjectWorkSession'],
    ) -> None:
        self.np_worksession = np_worksession
        self.ep_worksession = ep_worksession
    
    @staticmethod
    def from_dict(req: Dict) -> 'SignoutRequest':
        np_ws = [ 
             NewProjectWorkSession.from_dict(x) 
             for x in req.get('newProjectWorkSessions', []) 
        ]

        ep_ws = [ 
            ExistingProjectWorkSession.from_dict(x) 
            for x in req.get('existingProjectWorkSessions', []) 
        ]
            
        return SignoutRequest(np_ws, ep_ws)

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

class ConsumedMaterial:
    def __init__(self, material_id: int, quantity: int, units: str):
        self.material_id = material_id
        self.quantity = quantity
        self.units = units

    @staticmethod
    def from_dict(req) -> 'ConsumedMaterial':
        return ConsumedMaterial(
                req['materialId'],
                req['quantity'],
                req['units'],
        )


@bp.post('<visit_id>/_signout')
def signout(visit_id: int):
    visit_repo = VisitRepository(get_db())
    proj_repo = ProjectRepository(get_db())

    # Parse request
    signout_req = SignoutRequest.from_dict(flask.request.json)

    # This is a long request and MUST be wrapped in a transaction
    get_db().start_transaction()
    try:
        # End visit
        visit = visit_repo.load_by_id(visit_id)
        if visit.is_ended():
            return flask.abort(400, "The selected visit is already ended.")
        visit.end_time = dt.datetime.now()
        visit_repo.update(visit)

        # Convert New Projects to existing projects
        for new_project_session in signout_req.np_worksession:
            new_proj = new_project_session.project
            proj = proj_repo.create(new_proj.name, new_proj.description, new_proj.type)

            # Now that the project exists, move the work sessions to the update 
            # requests 
            signout_req.ep_worksession.append(ExistingProjectWorkSession(proj.project_id, new_project_session.equipment_use_log))

        # Drop all new sessions as they are now converted into exixting sessions
        signout_req.np_worksession = []
        

        # This is a translation from the reuqest model into the db model. It is 
        # not the clenest right now, and really needs the db model to be refactored
        print("Working sessions")
        for ex_project_session in signout_req.ep_worksession:
            project_update = VisitProject.create(get_db(), visit.visit_id, ex_project_session.project_id)

            if not ex_project_session.equipment_use_log:
                raise Exception("No equipment used exception")

            for eq_use_log in ex_project_session.equipment_use_log:
                eq_log = UsageLogEntry.create(get_db(), project_update.visit_project_id, eq_use_log.time_used.seconds)

                for mat_used in eq_use_log.consumed_material:
                    MaterialConsumed.create(
                            get_db(), 
                            mat_used.quantity, 
                            EquipmentMaterial.get_equipment_material_id(get_db(), eq_use_log.equipment_id, mat_used.material_id),
                            eq_log.usage_log_id
                    )

            print(ex_project_session)

        get_db().commit()
        return "ok"
    except:
        get_db().rollback()
        raise
