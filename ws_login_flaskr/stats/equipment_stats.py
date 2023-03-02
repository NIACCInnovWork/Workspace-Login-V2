from mysql.connector.connection import MySQLConnection
from ws_login_flaskr.stats.stats_registry import stat, Scaler, Point


@stat
class EquipmentUsage:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                equipment.*, 
                SUM(usage_log.time_used),
                COUNT(*)  
            FROM usage_log 
            JOIN materials_consumed 
                ON usage_log.usage_log_id = materials_consumed.usage_log_id 
            JOIN equipment_materials 
                ON equipment_materials.equipment_material_id = materials_consumed.equipment_material_id 
            JOIN equipment 
                ON equipment.equipment_id = equipment_materials.equipment_id 
            GROUP BY equipment.equipment_id, equipment.equipment_name;
        """

        cur = db.cursor()
        cur.execute(sql)
        points = [
            Point([
                Scaler("equipmentId", row[0]),
                Scaler("equipmentName", row[1]),
                Scaler("totalUseTime", int(row[2])),
                Scaler("numberOfUses", row[3]),
                Scaler("avgUseTime", int(row[2])/row[3]),
            ])
            for row in cur.fetchall()
        ]
        cur.close()
        return points


@stat
class EquipmentUsageByProjectType:
    def calculate(self, db: MySQLConnection):
        sql = """
            SELECT 
                equipment.equipment_id, 
                equipment.equipment_name, 
                projects.project_type,
                COUNT(*) as count,
                SUM(usage_log.time_used) as time_used
            -- Start with usage log as root entity
            FROM usage_log 
            -- Fetch equipment in usage log
            JOIN materials_consumed 
                ON usage_log.usage_log_id = materials_consumed.usage_log_id 
            JOIN equipment_materials 
                ON equipment_materials.equipment_material_id = materials_consumed.equipment_material_id 
            JOIN equipment 
                ON equipment.equipment_id = equipment_materials.equipment_id 

            -- Fetch project in useage usage_log
            JOIN visits_projects 
                ON usage_log.visit_project_id = visits_projects.visit_project_id
            JOIN projects
                ON visits_projects.project_id = projects.project_id
            GROUP BY equipment.equipment_id, equipment.equipment_name, projects.project_type
        """
        cur = db.cursor()
        cur.execute(sql)

        points = [
            Point([
                Scaler("equipmentId", row[0]),
                Scaler("equipmentName", row[1]),
                Scaler("projectType", row[2]),
                Scaler("count", row[3]),
                Scaler("timeUsed", int(row[4])),
            ])
            for row in cur.fetchall()
        ]
        cur.close()

        return points

