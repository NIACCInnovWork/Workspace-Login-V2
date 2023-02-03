import unittest
import os

from ws_login_client import ApiClient, UnknownStatError


def build_api_client() -> ApiClient:
    return ApiClient(
        os.environ.get("API_HOST", "https://workspace-login.riesenlabs.com"), 
        os.environ.get("API_TOKEN", "test-token")
    )


class TestStatsApiEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = build_api_client()
   
    def tearDown(self) -> None:
        self.api_client.close()

    def test_get_stats_list(self):
        expected_stats = [
                'AverageVisitsPerUser', 
                'EquipmentUsageByProjectType', 
                'TotalUsers', 
                'VisitsPerDayOfWeek', 
                'ProjectsByType', 
                'UsersByType', 
                'VisitsPerMonth', 
                'VisitsPerUserType', 
                'TrafficTimes', 
                'TotalProjects', 
                'EquipmentUsage', 
                'NewUsersByMonth', 
                'TotalVisits'
        ]

        stats = set(self.api_client.get_stats())
        for expected_stat in expected_stats:
            self.assertTrue(expected_stat in stats)

    def test_unknown_stat(self):
        with self.assertRaises(UnknownStatError):
            self.api_client.get_stat("DoesntExist")

    def test_average_visits_per_user(self):
        stat = self.api_client.get_stat("AverageVisitsPerUser")
        self.assertEqual(1, len(stat))
        self.assertEqual(float, type(stat[0]["visitsPerUser"]))

    def test_total_projects(self):
        stat = self.api_client.get_stat("TotalProjects")
        self.assertEqual(1, len(stat))
        self.assertEqual(int, type(stat[0]["TotalProjects"]))

    def test_total_users(self):
        stat = self.api_client.get_stat("TotalUsers")
        self.assertEqual(1, len(stat))
        self.assertEqual(int, type(stat[0]["TotalUsers"]))

    def test_total_visits(self):
        stat = self.api_client.get_stat("TotalVisits")
        self.assertEqual(1, len(stat))
        self.assertEqual(int, type(stat[0]["TotalVisits"]))

    def test_equipment_usage(self):
        stat = self.api_client.get_stat("EquipmentUsage")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["equipmentId"]))
            self.assertEqual(str, type(point["equipmentName"]))
            self.assertEqual(int, type(point["numberOfUses"]))
            self.assertEqual(int, type(point["totalUseTime"]))

    def test_equipment_usage_by_project_type(self):
        stat = self.api_client.get_stat("EquipmentUsageByProjectType")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(str, type(point["projectType"]))
            self.assertEqual(int, type(point["equipmentId"]))
            self.assertEqual(str, type(point["equipmentName"]))
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(int, type(point["timeUsed"]))

    def test_new_users_by_month(self):
        stat = self.api_client.get_stat("NewUsersByMonth")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(int, type(point["month"]))
            self.assertEqual(int, type(point["year"]))

    def test_projects_by_type(self):
        stat = self.api_client.get_stat("ProjectsByType")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["type"]))

    def test_traffic_times(self):
        stat = self.api_client.get_stat("TrafficTimes")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["day"]))
            self.assertEqual(int, type(point["hour"]))

    def test_users_by_type(self):
        stat = self.api_client.get_stat("UsersByType")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["type"]))

    def test_visits_per_day_of_week(self):
        stat = self.api_client.get_stat("VisitsPerDayOfWeek")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["dayOfWeek"]))
            self.assertEqual(float, type(point["persentage"]))

    def test_visits_per_month(self):
        stat = self.api_client.get_stat("VisitsPerMonth")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["month"]))
            self.assertEqual(int, type(point["year"]))


    def test_visits_per_user_type(self):
        stat = self.api_client.get_stat("VisitsPerUserType")
        self.assertGreater(len(stat), 0)
        for point in stat:
            self.assertEqual(int, type(point["count"]))
            self.assertEqual(str, type(point["type"]))


