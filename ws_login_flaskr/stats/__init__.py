"""
The stats module should be thought of as a seperate domain from the primary 
business domain.  Very few objects should overlap.

"""

import flask
from typing import Dict, List

from ws_login_flaskr.db import MySQLConnection, get_db

bp = flask.Blueprint('stats', __name__, url_prefix='/api/stats')

# Registry into which stats are loaded
from ws_login_flaskr.stats.stats_registry import stat, all_stats, Scaler, Point

# Stat file must be imported for stat to load
import ws_login_flaskr.stats.visits_per_month 
import ws_login_flaskr.stats.visits_per_day_of_week
import ws_login_flaskr.stats.traffic_times
import ws_login_flaskr.stats.users_by_type
import ws_login_flaskr.stats.traffic_times
import ws_login_flaskr.stats.projects_by_type
import ws_login_flaskr.stats.equipment_stats
import ws_login_flaskr.stats.new_users_by_month



@stat
class TotalUsers:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor()
        curr.execute("SELECT COUNT(*) FROM users;")
        user_count = curr.fetchone()[0]
        curr.close()

        return [Point([Scaler("TotalUsers", user_count)])]

@stat
class TotalVisits:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor()
        curr.execute("SELECT COUNT(*) FROM visits;")
        user_count = curr.fetchone()[0]
        curr.close()

        return [Point([Scaler("TotalVisits", user_count)])]

@stat
class TotalProjects:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor()
        curr.execute("SELECT COUNT(*) FROM projects;")
        user_count = curr.fetchone()[0]
        curr.close()

        return [Point([Scaler("TotalProjects", user_count)])]


@stat
class VisitsPerUserType:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor() 
        curr.execute("SELECT user_type, count(*) FROM users JOIN visits ON users.user_id = visits.user_id GROUP BY user_type;")
        
        points = [ Point([Scaler("type", row[0]), Scaler("count", row[1])]) for row in curr.fetchall() ]

        curr.close()
        return points

@stat
class AverageVisitsPerUser:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor()
        curr.execute("SELECT (SELECT COUNT(*) FROM visits) / (SELECT COUNT(*) FROM users);")
        row = curr.fetchone()
        points = [Point([Scaler("visitsPerUser", float(row[0]))])]
        curr.close()
        return points

@bp.get('')
def index() -> Dict[str, str]:
    return {key: f"{flask.request.host_url}api/stats/{key}" for key in all_stats.keys()}


@bp.get('/<stat_name>')
def executeStat(stat_name: str):
    if stat_name not in all_stats:
        return flask.abort(404, 'requested stat not found')

    stat_class = all_stats[stat_name]()

    points = stat_class.calculate(get_db())
    return [ p.to_dict() for p in points ]

