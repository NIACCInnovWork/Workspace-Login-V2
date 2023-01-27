""" API Smoke tests

The following test that the api is responding with valid data from most all 
query endpoints.  These tests **DO NOT WRITE ANYTHING** to the API.  This makes
them idempotent and safe to run repeatedly.

One artifact of them being read only tests is that the tests do assume that 
some data exists within the environment. Importantly, it assumes the following:

* There is at least one User, Project, Equipment
* The user "Anthony Riesen" exists and has at least one visit and project
* Project with id 10 exists

Configuration
=============
The api-token to use when fetching from the api is set through the "API_TOKEN"
environment variable
"""
import unittest
import os

from ws_login_client import ApiClient


class TestUserApiEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient("https://workspace-login.riesenlabs.com", os.environ.get("API_TOKEN"))

    def tearDown(self) -> None:
        self.api_client.close()

    def test_fetch_all_users_from_api(self):
        users = self.api_client.get_users()
        all_user_count = len(users)
        self.assertGreater(all_user_count, 0, "Expected more than 0 Users returned")

    def test_fetch_user_with_ongoing_visit_from_api(self):
        all_user_count = len(self.api_client.get_users())
        ongoing_users_count = len(self.api_client.get_users(ongoing=True))
        
        # Ideally this would assert greater than 0, but there may be no ongoing
        # visits
        msg = "Expected equal or more total users compared to ongoing users"
        self.assertGreaterEqual(all_user_count, ongoing_users_count, msg)

    def test_fetch_user_by_name_from_api(self):
        anthonys = self.api_client.get_users(name="Anthony Riesen")

        msg = "Expected exactly one user matching anthony"
        self.assertEqual(1, len(anthonys), msg)
        self.assertEqual("Anthony Riesen", anthonys[0].name)

    def test_fetch_user_by_id(self):
        anthony_sum = self.api_client.get_users(name="Anthony Riesen")[0]
        anthony = self.api_client.get_user(anthony_sum.id)

        self.assertEqual(anthony_sum.id, anthony.user_id)


class TestProjectApiEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient("https://workspace-login.riesenlabs.com", os.environ.get("API_TOKEN"))

    def tearDown(self) -> None:
        self.api_client.close()

    def test_fetch_all_projects(self):
        projects = self.api_client.get_projects()
        self.assertGreater(len(projects), 0)

    def test_fetch_project_by_id(self):
        # This is the terraform Tillage endpoint and is assumed to exist
        project = self.api_client.get_project(10)
        self.assertIsNotNone(project)

    def test_fetch_projects_for_a_user(self):
        anthony = self.api_client.get_user(self.api_client.get_users(name="Anthony Riesen")[0].id)
        anthonys_projects = self.api_client.get_projects_for(anthony)
        self.assertGreater(len(anthonys_projects), 0)


class TestVisitApiEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient("https://workspace-login.riesenlabs.com", os.environ.get("API_TOKEN"))

    def tearDown(self) -> None:
        self.api_client.close()

    def test_fetch_visits_for_user(self):
        anthony = self.api_client.get_user(self.api_client.get_users(name="Anthony Riesen")[0].id)
        anthonys_visits = self.api_client.get_visits_for(anthony)
        self.assertGreater(len(anthonys_visits), 0)

        # Testing ongoing visits is a bit tricky as the user may or may not 
        # have an ongoing visit. They should have only 1 or 0 though
        anthonys_ongoing_visits = self.api_client.get_visits_for(anthony, ongoing=True)
        self.assertTrue(len(anthonys_ongoing_visits) == 0 or len(anthonys_ongoing_visits) == 1)


class TestEquipmentApiEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = ApiClient("https://workspace-login.riesenlabs.com", os.environ.get("API_TOKEN"))

    def tearDown(self) -> None:
        self.api_client.close()

    def test_fetch_all_equipment(self):
        equipment = self.api_client.get_equipment()
        self.assertGreater(len(equipment), 0)

    def test_fetch_materials_for_equipment(self):
        equipment = self.api_client.get_equipment()[0]
        materials = self.api_client.get_materials_for(equipment)
        self.assertGreater(len(materials), 0)


