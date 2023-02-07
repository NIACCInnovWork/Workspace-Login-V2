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
            Scaler("count", row[1]),
            Scaler("avgUsers", self.avg_users_per_project_for_type(db, row[0])),
            Scaler("avgVisits", self.total_visits_for_type(db, row[0]) / row[1]),
        ]) for row in cur.fetchall() ]

        cur.close()

        return points
    
    def avg_users_per_project_for_type(self, db: MySQLConnection, type: str) -> float:
        # TODO WARNING!!! This is the thing making the request slow!!!
        sql = """
            SELECT AVG(user_count) 
            FROM (
                SELECT
                    projects.project_id,
                    COUNT(distinct user_id) AS user_count     
                FROM projects           
                JOIN visits_projects                   
                    ON projects.project_id = visits_projects.project_id           
                JOIN visits                   
                    ON visits_projects.visit_id = visits.visit_id           
                WHERE project_type = %s
                GROUP BY projects.project_id  
            ) users_per_project;
        """
        cur = db.cursor()
        cur.execute(sql, (type,))
        avg = float(cur.fetchone()[0])
        cur.close()
        return avg

    def total_visits_for_type(self, db: MySQLConnection, type: str) -> int:
        sql = """
            SELECT 
                count(*) 
            FROM projects 
            JOIN visits_projects 
                ON projects.project_id = visits_projects.project_id 
            WHERE project_type = %s;
            """
        cur = db.cursor()
        cur.execute(sql, (type,))
        total = cur.fetchone()[0]
        cur.close()

        return total 
