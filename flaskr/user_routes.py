from flask import Blueprint, abort
from flaskr.db import get_db

from database.class_user import UserRepository

bp = Blueprint('users', __name__, url_prefix = '/api/users')

@bp.get('')
def get_users():
    db = get_db()
    user_repo = UserRepository(db)
    return user_repo.get_all_visitors()


@bp.get("/<user_id>")
def get_user(user_id):
    db = get_db()
    user_repo = UserRepository(db)
    user = user_repo.load(user_id)
    if user is None:
        abort(404)
    return {
        "userId": user.user_id,
        "dateJoined": user.date_joined,
        "name": user.name,
        "userType": str(user.user_type),
    }
