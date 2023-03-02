from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point

_months_of_year = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
        }

@stat
class VisitsPerMonth:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                YEAR(start_time),
                MONTH(start_time),
                COUNT(*)
            FROM visits 
            GROUP BY YEAR(start_time), MONTH(start_time)
            ORDER BY YEAR(start_time), MONTH(start_time);
            """
        cur = db.cursor()
        cur.execute(sql)
        points = [ Point([
            Scaler("year", row[0]),
            Scaler("month", _months_of_year[row[1]]),
            Scaler("count", row[2]),
        ]) for row in cur.fetchall() ]
        cur.close()
        return points
