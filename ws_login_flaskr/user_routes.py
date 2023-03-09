import flask
import datetime as dt

from ws_login_flaskr.db import get_db
from ws_login_flaskr.repositories import VisitRepository, UserRepository, ProjectRepository
from ws_login_domain import  User, UserSummary, UserType

from ws_login_flaskr.repositories.matchpolicy import UserMatchPolicy, VisitMatchPolicy


from typing import Dict

bp = flask.Blueprint('users', __name__, url_prefix = '/api/users')


def _user_to_response(host_url, user: User):
    return {
        "userId": user.user_id,
        "dateJoined": user.date_joined.isoformat(),
        "name": user.name,
        "userType": user.user_type.name,
        "visitsRef": f"{host_url}api/users/{user.user_id}/visits",
        "projectsRef": f"{host_url}api/users/{user.user_id}/projects",
    }

def _user_summary_to_response(host_url, user: UserSummary):
    return {
        "id": user.id,
        "name": user.name,
        "ref": f"{host_url}api/users/{user.id}"
    }


@bp.get('')
def get_users():
    user_repo = UserRepository(get_db())

    match_policy = UserMatchPolicy.ALL()
    if flask.request.args.get("ongoing") == 'true':
        match_policy = UserMatchPolicy.ONGOING()
    elif flask.request.args.get("ongoing") == 'false':
        match_policy = UserMatchPolicy.NOT_ONGOING()

    if "name" in flask.request.args:
        match_policy = match_policy.with_name(flask.request.args["name"])

    return [
        _user_summary_to_response(flask.request.host_url, user)
        for user in user_repo.get_all_visitors(match_policy)
    ]


@bp.post('')
def create_user():
    new_user_json = flask.request.json

    if 'id' in new_user_json or 'name' not in new_user_json or 'type' not in new_user_json:
        return flask.abort(400, "Feild requirements not satisfied")

    user_repo = UserRepository(get_db())
    date_joined = dt.datetime.fromisoformat(new_user_json['dateJoined']) if 'dateJoined' in new_user_json else dt.datetime.now()
    user = user_repo.create(new_user_json['name'], UserType[new_user_json['type']], date_joined)

    return _user_to_response(flask.request.host_url, user)


@bp.put('/<user_id>')
def update_user(user_id: int):
    user_repo = UserRepository(get_db())
    user = user_repo.load(user_id)
    update = flask.request.json
    if user is None:
        flask.abort(404)
    elif update is None:
        flask.abort(400)

    user.name = update.get('name', user.name)
    user.user_type = UserType[update.get('type', user.user_type.name)]

    user_repo.update(user)

    return _user_to_response(flask.request.host_url, user)


@bp.get("/<user_id>")
def get_user(user_id):
    user_repo = UserRepository(get_db())
    user = user_repo.load(user_id)
    if user is None:
        flask.abort(404)
    return _user_to_response(flask.request.host_url, user)


@bp.get("/<user_id>/visits")
def get_visits(user_id: int):
    user_repo = UserRepository(get_db())
    visit_repo = VisitRepository(get_db())

    match_policy = VisitMatchPolicy.ALL()
    if flask.request.args.get("ongoing") == 'true':
        match_policy = VisitMatchPolicy.ONGOING()
    elif flask.request.args.get("ongoing") == 'false':
        match_policy = VisitMatchPolicy.NOT_ONGOING()

    user = user_repo.load(user_id)
    visits = visit_repo.load_by_user(user, match_policy)

    return [
        {
            "id": visit.visit_id,
            "startTime": visit.start_time.isoformat(),
            "endTime": visit.end_time.isoformat() if visit.end_time else None,
        }
        for visit in visits
    ]


@bp.post("/<user_id>/visits")
def create_visit(user_id: int):
    user_repo = UserRepository(get_db())
    visit_repo = VisitRepository(get_db())

    new_visit_req = flask.request.json
    visit_start_time = dt.datetime.fromisoformat(new_visit_req['startTime']) if 'startTime' in new_visit_req else dt.datetime.now()

    user = user_repo.load(user_id)
    if not user:
        return flask.abort(404, "The specified user was not found")
    ongoing_visits = visit_repo.load_by_user(user, VisitMatchPolicy.ONGOING())
    if ongoing_visits: 
        return flask.abort(400, "There is currently a visit in progress. That visit must be finished before creating a new one.")

    visit = visit_repo.create_for(user, visit_start_time)

    return {
        "id": visit.visit_id,
        "startTime": visit.start_time.isoformat(),
        "endTime": visit.end_time.isoformat() if visit.end_time else None,
    }


@bp.get("/<user_id>/projects")
def get_projects(user_id: int):
    user_repo = UserRepository(get_db())
    proj_repo = ProjectRepository(get_db())

    user = user_repo.load(user_id)
    projects = proj_repo.load_for(user)

    return [
        {
            "id": proj.id,
            "name": proj.name,
            "ref": f"{flask.request.host_url}api/projects/{proj.id}",
        }
        for proj in projects
    ]
