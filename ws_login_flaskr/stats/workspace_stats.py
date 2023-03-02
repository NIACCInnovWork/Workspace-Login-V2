from typing import List

from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point

@stat
class WorkspaceStats:
    def calculate(self, db: MySQLConnection) -> List[Point]:
        sql = """
        SELECT 
            (SELECT COUNT(*) FROM users) AS total_users,
            (SELECT COUNT(*) FROM visits) AS total_visits,
            (SELECT COUNT(*) FROM projects) AS total_projects
        """
        curr = db.cursor()
        curr.execute(sql)
        row = curr.fetchone()
        curr.close()

        return [Point([
            Scaler("totalUsers", row[0]),
            Scaler("totalVisits", row[1]),
            Scaler("totalProjects", row[2]),
            Scaler("avgVisitsPerUser", row[2]/row[0]),
        ])]

