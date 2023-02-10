import flask
from typing import List, Dict
import datetime as dt

from ws_login_domain import Project, ProjectType
from ws_login_domain.requests import SignoutRequest, ExistingProjectWorkSession

from ws_login_flaskr.db import get_db
from ws_login_flaskr.repositories import VisitRepository, ProjectRepository

# TODO still need to be refactored
from ws_login_flaskr.repositories.class_material_consumed import MaterialConsumed
from ws_login_flaskr.repositories.class_usage_log_entry import UsageLogEntry
from ws_login_flaskr.repositories.class_visit_project import VisitProject
from ws_login_flaskr.repositories.class_equipment_material import EquipmentMaterial
from ws_login_flaskr.repositories.class_usage_log_entry import UsageLogEntry


bp = flask.Blueprint('visits', __name__, url_prefix = '/api/visits')

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

@bp.post('<visit_id>/_signout')
def signout(visit_id: int):
    visit_repo = VisitRepository(get_db())
    proj_repo = ProjectRepository(get_db())

    # Parse request
    signout_req = SignoutRequest.from_dict(visit_id, flask.request.json)

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

        get_db().commit()
        return "ok"
    except:
        get_db().rollback()
        raise
