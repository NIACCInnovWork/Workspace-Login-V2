from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point


@stat
class NewUsersByMonth:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                YEAR(date_joined), 
                MONTH(date_joined), 
                COUNT(*) 
            FROM users 
            GROUP BY YEAR(date_joined), MONTH(date_joined);
        """

        cur = db.cursor()
        cur.execute(sql)
        points = [
            Point([
                Scaler("year", row[0]),
                Scaler("month", row[1]),
                Scaler("count", row[2]),
            ])
            for row in cur.fetchall()
        ]
        cur.close()

        return points
