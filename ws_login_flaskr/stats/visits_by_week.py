from flask import request


from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point



@stat
class VisitsByWeek:
    def calculate(self, db: MySQLConnection):
        is_include_workstudy = request.args.get('include-workstudy').lower() == 'true'

        exclude_workstudy_sql = """
            WHERE EXISTS (     
                SELECT *           
                FROM visits_projects           
                JOIN projects          
                      ON visits_projects.project_id = projects.project_id               
                WHERE             
                    visits_projects.visit_id = visits.visit_id                   
                    AND projects.project_type != 'WorkStudy'
                )
        """
        sql = """
            SELECT 
                YEAR(start_time), 
                WEEK(start_time), 
                COUNT(DISTINCT user_id) AS unique_visitors, 
                COUNT(*) AS total_visits,
                SUM(TIMESTAMPDIFF(SECOND, start_time, end_time)) AS total_time
            FROM visits 
            {workstudy_filter}
            GROUP BY YEAR(start_time), WEEK(start_time) 
            ORDER BY YEAR(start_time), WEEK(start_time);
        """.format(workstudy_filter=exclude_workstudy_sql if not is_include_workstudy else "")
        print(sql)

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
