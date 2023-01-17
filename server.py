import flask
from flask import Flask
from database.class_user import User
from database.initialize_database import start_workspace_database
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/users")
def get_users():
    conn = start_workspace_database()
    return User.get_all_visitors(conn)


@app.route("/users")
def get_users_page():
    conn = start_workspace_database()
    return flask.render_template('users_page.html', users=User.get_all_visitors(conn))


@app.route("/api/users/<user_id>")
def get_user(user_id):
    conn = start_workspace_database()
    user = User.load(conn, user_id)
    if user is None:
        flask.abort(404)
    return {
        "userId": user.user_id,
        "dateJoined": user.date_joined,
        "name": user.name,
        "userType": str(user.user_type),
    }
