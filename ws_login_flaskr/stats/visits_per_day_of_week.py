from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point


_days_of_week = {
        1: "Sunday",
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        7: "Saturday",
}

@stat
class VisitsPerDayOfWeek:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                DAYOFWEEK(start_time),
                COUNT(*)
            FROM visits 
            GROUP BY DAYOFWEEK(start_time)
            ORDER BY DAYOFWEEK(start_time);
            """

        cur = db.cursor()
        cur.execute(sql)

        rows = cur.fetchall()
        cur.close()
        
        # This could probably be done in the query directly, but it was easy 
        # enough to just do in software
        total = sum(map(lambda r: r[1], rows))

        return [ Point([
            Scaler("dayOfWeek", _days_of_week[row[0]]),
            Scaler("count", row[1]),
            Scaler("persentage", (row[1] / total) * 100),
        ]) for row in rows ]

