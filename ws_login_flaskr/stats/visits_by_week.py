
from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point

@stat
class VisitsByWeek:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                YEAR(start_time), 
                WEEK(start_time), 
                COUNT(DISTINCT user_id) AS unique_visitors, 
                COUNT(*) AS total_visits,
                SUM(TIMESTAMPDIFF(SECOND, start_time, end_time)) AS total_time
            FROM visits 
            GROUP BY YEAR(start_time), WEEK(start_time) 
            ORDER BY YEAR(start_time), WEEK(start_time);
        """

        cur = db.cursor()
        cur.execute(sql)

        points = [
            Point([
                Scaler("year", row[0]),
                Scaler("week", row[1]),
                Scaler("uniqueVisitors", row[2]),
                Scaler("totalVisits", row[3]),
                Scaler("totalVisitTime", int(row[4])),
            ])
            for row in cur.fetchall()
        ]
        cur.close()

        return points
