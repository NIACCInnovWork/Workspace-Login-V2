import flask
from flask import Blueprint, abort
from database.class_project import ProjectRepository
from flaskr.db import get_db

from database.class_user import UserRepository

bp = Blueprint('projects', __name__, url_prefix = '/api/projects')

@bp.get('')
def get_projects():
    db = get_db()
    project_repo = ProjectRepository(db)
    return [
        {
            "id": proj.id,
            "name": proj.name,
            "ref": f"{flask.request.host_url}api/projects/{proj.id}",
        }
        for proj in project_repo.load_all_projects()
    ]


@bp.get("/<project_id>")
def get_project(project_id):
    db = get_db()
    project_repo = ProjectRepository(db)
    project = project_repo.load(project_id)
    if project is None:
        abort(404)

    return {
        "id": project.project_id,
        "name": project.project_name,
        "description": project.project_description,
        "type": str(project.project_type),
    }
