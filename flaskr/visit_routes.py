import flask
from flask import Blueprint, abort

from flaskr.db import get_db
from database.class_visit import VisitRepository

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


@bp.post('<visit_id>/_signout')
def signout(visit_id: int):
    return "ok"
