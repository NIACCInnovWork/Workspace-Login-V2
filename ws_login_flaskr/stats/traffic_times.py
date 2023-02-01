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
class TrafficTimes:
    def calculate(self, db: MySQLConnection):
        # This is just going to pull all visits and agregate them to make the 
        # logic easier, this will undoutedly need to be made more efficent in 
        # the future.
        sql = "SELECT start_time, end_time FROM visits;"

        agg = {
            1: [0] * 24, # Sunday
            2: [0] * 24, # Monday
            3: [0] * 24, # Tuesday
            4: [0] * 24, # Wednesday
            5: [0] * 24, # Thursday
            6: [0] * 24, # Friday
            7: [0] * 24, # Saturday
        }
        cur = db.cursor()
        cur.execute(sql)
        
        # Mark every hour for which a user was present
        rows = cur.fetchmany(100)
        while rows:
            for (start_time, end_time) in rows:
                # Day of week from the database DAYOFWEEK function was indexed 
                # from 1, so we will stick with that
                day_record = agg[start_time.weekday() + 1]
                for hour in range(start_time.hour, end_time.hour + 1):
                    day_record[hour] += 1

            rows = cur.fetchmany(100)
        cur.close()
        
        # Convert into stats representation
        points = []
        for dow in range(1, 7 + 1):
            for hour, count in enumerate(agg[dow]):
                points.append(Point([
                        Scaler("day", _days_of_week[dow]),
                        Scaler("hour", hour), # in 24 hour
                        Scaler("count", count), # total ongoing visits at that hour
                ]))

        return points

