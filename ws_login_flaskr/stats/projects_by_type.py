from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point


@stat
class ProjectsByType:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                project_type,
                COUNT(*)
            FROM projects
            GROUP BY project_type
            """

        cur = db.cursor()
        cur.execute(sql)

        points = [ Point([
            Scaler("type", row[0]),
            Scaler("count", row[1])
        ]) for row in cur.fetchall() ]

        cur.close()

        return points

