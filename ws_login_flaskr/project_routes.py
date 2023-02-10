import flask

from ws_login_flaskr.db import get_db
from ws_login_flaskr.repositories import ProjectRepository, UserRepository

bp = flask.Blueprint('projects', __name__, url_prefix = '/api/projects')

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
        flask.abort(404)

    return {
        "id": project.project_id,
        "name": project.project_name,
        "description": project.project_description,
        "type": project.project_type.name,
    }
