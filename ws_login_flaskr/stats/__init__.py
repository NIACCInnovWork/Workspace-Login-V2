"""
The stats module should be thought of as a seperate domain from the primary 
business domain.  Very few objects should overlap.

"""

import flask
from typing import Dict, List

from ws_login_flaskr.db import MySQLConnection, get_db

bp = flask.Blueprint('stats', __name__, url_prefix='/api/stats')

all_stats = {}

class Scaler:
    def __init__(self, demention: str, value: any):
        self.demention = demention
        self.value = value


class Point:
    def __init__(self, coordinates: List[Scaler]):
        self.coordinates = coordinates

    def to_dict(self) -> Dict:
        return { c.demention: c.value for c in self.coordinates }


def stat(stat_class):
    all_stats[stat_class.__name__] = stat_class

    return stat_class


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
class VisitsPerUserType:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        curr = db.cursor()
        curr.execute("SELECT user_type, count(*) FROM users JOIN visits ON users.user_id = visits.user_id GROUP BY user_type;")
        
        points = [ Point([Scaler("type", row[0]), Scaler("count", row[1])]) for row in curr.fetchall() ]

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

