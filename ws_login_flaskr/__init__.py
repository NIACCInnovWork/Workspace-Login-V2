import flask
import flask_login
import os
import logging

from urllib.parse import urlparse

from ws_login_flaskr.db import get_db, close_db
from ws_login_flaskr.permission import admin, has_permission, superuser, SystemUser
from ws_login_flaskr.repositories.user_repository import UserRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = flask.Flask(__name__)
    app.teardown_appcontext(close_db)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # TODO change it!!!

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def fetch_user(user_id: str):
        if user_id == '-1':
            return admin
        if user_id == '-2':
            return superuser

        # Returns `None` if the user does not exist
        user_repo = UserRepository(get_db())
        user = user_repo.load(int(user_id))
        if user:
            return SystemUser(user.user_id, user.name, [], False)
        logger.warning(f"Session attempted to use user id {user_id} which does not exist")
        return None

    @app.before_request
    def check_token():
        """ Primitive "auth" check before serviceing requests.

        The client must supply an api-token as a cookie matching the token with 
        which the service was initialized.  If this is not the case, a 401 
        response is returned.

        A few requests are allowed through dispite not having authorization. 
        These are:
            * /api/healthcheck
            * /api/init
        """
        route = flask.request.path
        if route == "/api/healthcheck" or route == "/api/init" or route == "/api/login": 
            return

        if flask.request.cookies.get("api-token") != os.environ.get("API_TOKEN", "test-token") \
                and flask_login.current_user.is_anonymous:
            flask.abort(401, "No access token found or incorrect access token")

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
            "Stats": f"{flask.request.host_url}api/stats",
        }

    @app.route("/api/healthcheck")
    def healthcheck():
        """ Provides health check. Returns 200 if service is running.

        No authentication is set on this endpoint.
        """
        return { "status": "ok" }

    @app.route("/api/init")
    def init():
        """ Provides a way for a user to initialize there brower through an 
        "authorized" link.

        Access to the application is guarded by a simple api-token which is 
        globally used. This token is provided to the application via a cookie.

        This endpoint allows the api-token to be encoded in a link, which can 
        be more easily shared. The response instructs the browser to store the 
        token as a cookie and then redirects the application to '/'.
        """
        api_token = flask.request.args.get('api-token')
        if api_token != os.environ.get("API_TOKEN", "test-token"):
            flask.abort(401, "No access token found or incorrect access token")

        resp = flask.make_response(flask.redirect("/", code=302))
        resp.set_cookie('api-token', flask.request.args.get('api-token'))
        return resp

    @app.route("/api/login")
    def login():
        """ Provides a way for a user to initialize there brower through an 
        "authorized" link.

        Access to the application is guarded by a simple api-token which is 
        globally used. This token is provided to the application via a cookie.

        This endpoint allows the api-token to be encoded in a link, which can 
        be more easily shared. The response instructs the browser to store the 
        token as a cookie and then redirects the application to '/'.
        """
        api_token = flask.request.args.get('api-token')
        if api_token == os.environ.get("API_TOKEN", "test-token"):
            flask_login.login_user(admin)
            return flask.redirect("/", code=302)
        
        if api_token == os.environ.get("API_TOKEN_SUPER", "test-token-super"):
            flask_login.login_user(superuser)
            return flask.redirect("/", code=302)

        print("Attempted to login without token")
        return flask.abort(401, "No access token found or incorrect access token")


    @app.route("/api/about")
    def about():
        return {
            "Description": "Login and equipment usage tracker for the Inovation Workspace",
            "Api Documentation": "TODO",
            "Version": "1.0.0",
        }


    @app.route("/api/super")
    @has_permission('superuser')
    def super_test():
        """ Temp endpoint

        This endpoint is just here to test if the superuser permission works.
        """
        return {"msg": "supper users only"}

    from ws_login_flaskr.user_routes import bp as user_routes_bp
    from ws_login_flaskr.project_routes import bp as project_routes_bp
    from ws_login_flaskr.equipment_routes import bp as equipment_routes_bp
    from ws_login_flaskr.visit_routes import bp as visit_routes_bp
    app.register_blueprint(user_routes_bp)
    app.register_blueprint(project_routes_bp)
    app.register_blueprint(equipment_routes_bp)
    app.register_blueprint(visit_routes_bp)

    # The stats domain should be thought of as seperate 
    from ws_login_flaskr.stats import bp as stats_bp
    app.register_blueprint(stats_bp)

    return app

