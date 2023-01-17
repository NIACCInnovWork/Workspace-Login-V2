import flask
from flask import Blueprint, abort
from flaskr.db import get_db

from database.class_user import UserRepository, User, UserSummary, UserType

from typing import Dict

bp = Blueprint('users', __name__, url_prefix = '/api/users')


def _user_to_response(user: User):
    return {
        "userId": user.user_id,
        "dateJoined": user.date_joined,
        "name": user.name,
        "userType": user.user_type.name,
    }

def _user_summary_to_response(host_url, user: UserSummary):
    return {
        "id": user.id,
        "name": user.name,
        "ref": f"{flask.request.host_url}api/users/{user.id}"
    }


@bp.get('')
def get_users():
    user_repo = UserRepository(get_db())
    return [
        _user_summary_to_response(flask.request.host_url, user)
        for user in user_repo.get_all_visitors()
    ]


@bp.post('')
def create_user():
    new_user_json = flask.request.json

    if 'id' in new_user_json or 'name' not in new_user_json or 'type' not in new_user_json:
        return abort(400, "Feild requirements not satisfied")

    user_repo = UserRepository(get_db())
    user = user_repo.create(new_user_json['name'], UserType[new_user_json['type']])

    return _user_to_response(user)


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

    return _user_to_response(user)    


@bp.get("/<user_id>")
def get_user(user_id):
    db = get_db()
    user_repo = UserRepository(db)
    user = user_repo.load(user_id)
    if user is None:
        abort(404)
    return _user_to_response(user)
