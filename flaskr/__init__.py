import flask
from flask import Flask

from urllib.parse import urlparse

from flaskr.db import close_db


def create_app():
    app = Flask(__name__)
    app.teardown_appcontext(close_db)

    @app.route("/")
    def redirect_to_api():
        return flask.redirect("/api", code=302)

    @app.route("/api")
    def main_routes():
        return {
            "Users": f"{flask.request.host_url}api/users",
            "Projects": f"{flask.request.host_url}api/projects"
        }

    from flaskr.user_routes import bp as user_routes_bp
    from flaskr.project_routes import bp as project_routes_bp
    app.register_blueprint(user_routes_bp)
    app.register_blueprint(project_routes_bp)

    return app
