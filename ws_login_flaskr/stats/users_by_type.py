from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point


@stat
class UsersByType:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                user_type,
                COUNT(*)
            FROM users 
            GROUP BY user_type 
            """

        cur = db.cursor()
        cur.execute(sql)

        points = [ Point([
            Scaler("type", row[0]),
            Scaler("count", row[1]),
        ]) for row in cur.fetchall() ]

        cur.close()

        return points

