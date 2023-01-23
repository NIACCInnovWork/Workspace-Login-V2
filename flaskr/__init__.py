import flask
import os

from urllib.parse import urlparse

from flaskr.db import close_db


def create_app():
    app = flask.Flask(__name__)
    app.teardown_appcontext(close_db)

    @app.before_request
    def check_token():
        if flask.request.path == "/api/healthcheck":
            return

        if flask.request.cookies.get("api-token") != os.environ.get("API_TOKEN", "test-token"):
            return flask.abort(401, "No access token found or incorrect access token")

    @app.route("/")
    def redirect_to_api():
        return flask.redirect("/api", code=302)

    @app.route("/api")
    def main_routes():
        return {
            "Users": f"{flask.request.host_url}api/users",
            "Projects": f"{flask.request.host_url}api/projects",
            "Equipment": f"{flask.request.host_url}api/equipment",
            "Visits": f"{flask.request.host_url}api/visits",
            "About": f"{flask.request.host_url}api/about",
            "Healthcheck": f"{flask.request.host_url}api/healthcheck",
        }

    @app.route("/api/healthcheck")
    def healthcheck():
        return { "status": "ok" }

    @app.route("/api/about")
    def about():
        return {
            "Description": "Login and equipment usage tracker for the Inovation Workspace",
            "Api Documentation": "TODO",
            "Version": "1.0.0",
        }

    from flaskr.user_routes import bp as user_routes_bp
    from flaskr.project_routes import bp as project_routes_bp
    from flaskr.equipment_routes import bp as equipment_routes_bp
    from flaskr.visit_routes import bp as visit_routes_bp
    app.register_blueprint(user_routes_bp)
    app.register_blueprint(project_routes_bp)
    app.register_blueprint(equipment_routes_bp)
    app.register_blueprint(visit_routes_bp)

    return app
