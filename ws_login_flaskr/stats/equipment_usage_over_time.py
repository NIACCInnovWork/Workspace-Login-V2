from flask import request


from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point



@stat
class EquipmentUsageOverTime:
    def calculate(self, db: MySQLConnection):
        # Default bin by month, but optionaly bin by week
        # TODO fix hacky fetch from request global
        bin_by = 'month'
        bin_by_sql = 'MONTH(start_time)'
        if request.args.get('bin-by', 'month').lower() == 'week':
            bin_by = 'week'
            bin_by_sql = 'WEEK(start_time)'
        print('Bin By: ' + bin_by)
        
        sql = """
        SELECT 
            equipment.equipment_id, 
            equipment_name,
            YEAR(start_time) AS year,
            {bin_by_sql} as {bin_by},
            COUNT(*) AS total_uses,
            SUM(time_used) AS total_time_used
        FROM visits 
        JOIN visits_projects 
            ON visits.visit_id = visits_projects.visit_id 
        JOIN usage_log 
            ON visits_projects.visit_project_id = usage_log.visit_project_id
        JOIN materials_consumed 
            ON usage_log.usage_log_id = materials_consumed.usage_log_id 
        JOIN equipment_materials 
            ON materials_consumed.equipment_material_id = equipment_materials.equipment_material_id 
        JOIN equipment 
            ON equipment_materials.equipment_id = equipment.equipment_id
        GROUP BY
            equipment.equipment_id, 
            equipment_name,
            YEAR(start_time),
            {bin_by_sql}
        ORDER BY
            YEAR(start_time),
            {bin_by_sql},
            equipment.equipment_id;
        """.format(bin_by_sql=bin_by_sql, bin_by=bin_by)
        cur = db.cursor()
        cur.execute(sql)

        points = [
            Point([
                Scaler("equipmentId", row[0]),
                Scaler("equipmentName", row[1]),
                Scaler("year", row[2]),
                Scaler(bin_by, row[3]),
                Scaler("totalUses", row[4]),
                Scaler("totalTimeUsed", int(row[5])),
            ])
            for row in cur.fetchall()
        ]
        cur.close()
        
        return points
