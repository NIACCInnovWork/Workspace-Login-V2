from flask import Flask
from flaskr.db import close_db


def create_app():
    app = Flask(__name__)
    app.teardown_appcontext(close_db)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    from flaskr.user_routes import bp as user_routes_bp
    app.register_blueprint(user_routes_bp)

    return app
