import flask
from flask import Blueprint, abort
from database.class_visit import VisitRepository 
from database.matchpolicy import MatchPolicy
from flaskr.db import get_db

from database.class_user import UserRepository, User, UserSummary, UserType
from database.class_project import ProjectRepository

from typing import Dict

bp = Blueprint('users', __name__, url_prefix = '/api/users')


def _user_to_response(host_url, user: User):
    return {
        "userId": user.user_id,
        "dateJoined": user.date_joined,
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

    match_policy = MatchPolicy.ALL()
    if flask.request.args.get("ongoing") == 'true':
        match_policy = MatchPolicy.ONGOING()
    elif flask.request.args.get("ongoing") == 'false':
        match_policy = MatchPolicy.NOT_ONGOING()

    if "name" in flask.request.args:
        match_policy = match_policy.with_name(flask.request.args["name"])

    return [
        _user_summary_to_response(flask.request.host_url, user)
        for user in user_repo.get_all_visitors(match_policy)
    ]


@bp.post('')
def create_user():
    new_user_json = flask.request.json
    print(new_user_json)

    if 'id' in new_user_json or 'name' not in new_user_json or 'type' not in new_user_json:
        return abort(400, "Feild requirements not satisfied")

    user_repo = UserRepository(get_db())
    user = user_repo.create(new_user_json['name'], UserType[new_user_json['type']])

    return _user_to_response(flask.request.host_url, user)


@bp.put('/<user_id>')
def update_user(user_id: int):
    user_repo = UserRepository(get_db())
    user = user_repo.load(user_id)
    update = flask.request.json
    if user is None:
        abort(404)
    elif update is None:
        abort(400)

    user.name = update.get('name', user.name)
    user.user_type = UserType[update.get('type', user.user_type.name)]

    user_repo.update(user)

    return _user_to_response(flask.request.host_url, user)


@bp.get("/<user_id>")
def get_user(user_id):
    user_repo = UserRepository(get_db())
    user = user_repo.load(user_id)
    if user is None:
        abort(404)
    return _user_to_response(flask.request.host_url, user)


@bp.get("/<user_id>/visits")
def get_visits(user_id: int):
    user_repo = UserRepository(get_db())
    visit_repo = VisitRepository(get_db())

    match_policy = MatchPolicy.ALL()
    if flask.request.args.get("ongoing") == 'true':
        match_policy = MatchPolicy.ONGOING()
    elif flask.request.args.get("ongoing") == 'false':
        match_policy = MatchPolicy.NOT_ONGOING()

    user = user_repo.load(user_id)
    visits = visit_repo.load_by_user(user, match_policy)

    return [
        {
            "id": visit.visit_id,
            "startTime": visit.start_time,
            "endTime": visit.end_time,
        }
        for visit in visits
    ]


@bp.post("/<user_id>/visits")
def create_visit(user_id: int):
    user_repo = UserRepository(get_db())
    visit_repo = VisitRepository(get_db())

    user = user_repo.load(user_id)
    if not user:
        return flask.abort(404, "The specified user was not found")
    ongoing_visits = visit_repo.load_by_user(user, MatchPolicy.ONGOING())
    if ongoing_visits: 
        return flask.abort(400, "There is currently a visit in progress. That visit must be finished before creating a new one.")

    visit = visit_repo.create_for(user)

    print("Createing new visit")
    return {
        "id": visit.visit_id,
        "startTime": visit.start_time,
        "endTime": visit.end_time,
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
        }
        for proj in projects
    ]
