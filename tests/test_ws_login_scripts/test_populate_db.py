import unittest
from unittest.mock import Mock, call, ANY
import datetime as dt
from faker import Faker
from typing import Optional

from ws_login_domain import User, UserType, Equipment, Material, Visit, ProjectSummary, Project, ProjectType
from ws_login_domain.requests import SignoutRequest
from ws_login_scripts.populate_db import UserFactory, EquipmentAndMaterials
import ws_login_scripts.populate_db as script


def fake_user_gen(name: str, user_type: UserType, date_joined: Optional[dt.datetime] = None):
    user_id = 1
    if not date_joined:
        date_joined = dt.datetime.now()
    return User(user_id, date_joined, name, user_type)

class TestUserFactory(unittest.TestCase):

    def setUp(self):
        self.api_client = Mock()
        self.api_client.get_users.return_value = []
        self.api_client.create_user.side_effect = fake_user_gen

    def test_two_consecutive_users_arnt_identical(self):
        user_factory = UserFactory(self.api_client, Faker())
        userA = next(user_factory)
        userB = next(user_factory)

        self.assertNotEqual(userB, userA)

    def test_factory_doesnt_insert_users_if_they_already_exist(self):
        self.api_client.get_users.side_effect = [[fake_user_gen("foo", UserType.Student)], []]

        user_factory = UserFactory(self.api_client, Faker())
        user = next(user_factory)

        self.api_client.get_users.assert_has_calls([call(name=ANY), call(name=ANY)])

    def test_factory_only_generates_up_to_the_configured_number_of_elements(self):
        user_factory = UserFactory(self.api_client, Faker(), 5)

        all_users = [ user for user in user_factory ]

        self.assertEqual(5, len(all_users))


class TestEquipmentAndMaterials(unittest.TestCase):
    def test_contains_eq_and_materials(self):
        equipment = Equipment(5, "foobar")
        material = Material(2, "something", "in2")

        eq = EquipmentAndMaterials(equipment, [material])

        self.assertEqual(eq.equipment, equipment)
        self.assertEqual(eq.material, [material])


class TestFetchEquipmentAndMaterials(unittest.TestCase):
    def test_fetch_equipment_from_api(self):
        equipment = Equipment(5, "foobar")
        material = Material(2, "something", "in2")

        api_client = Mock()
        api_client.get_equipment.return_value = [equipment]
        api_client.get_materials_for.return_value = [material]

        result = script.fetch_equipment_and_materials(api_client)

        self.assertEqual([EquipmentAndMaterials(equipment, [material])], result)
        api_client.get_materials_for.assert_called_with(equipment)


class TestSelectWorkSessions(unittest.TestCase):
    def test_creates_new_project_if_none_exist(self):
        api_client = Mock()
        api_client.get_projects_for.return_value = []
        api_client.get_projects.return_value = []

        user = User(1, dt.datetime(2022, 1, 1), "foobar", UserType.Student)
        visit = Visit(1, user.user_id, dt.datetime.now(), None)
        signout_req = SignoutRequest.for_visit(visit)

        ws = script.generate_worksession(api_client, Faker(), signout_req, user)

        self.assertIsNotNone(ws)
        self.assertTrue(ws in signout_req.np_worksession)

    def test_if_projects_exist_an_existing_project_is_used(self):
        api_client = Mock()
        api_client.get_projects_for.return_value = [ProjectSummary(1, "foobar")]
        api_client.get_projects.return_value = [ProjectSummary(1, "foobar")]
        api_client.get_project.return_value = Project(1, "foobar", "description", ProjectType.Personal)

        user = User(1, dt.datetime(2022, 1, 1), "foobar", UserType.Student)
        visit = Visit(1, user.user_id, dt.datetime.now(), None)
        signout_req = SignoutRequest.for_visit(visit)

        ws = script.generate_worksession(api_client, Faker(), signout_req, user)

        self.assertIsNotNone(ws)
        self.assertTrue(ws in signout_req.ep_worksession)



def create_fake_visit(user: User, start_time: Optional[dt.datetime]):
    # Check expected time range
    assert user.date_joined < start_time and start_time < dt.datetime.now()
    return Visit(1, user.user_id, start_time, None)

def fake_signout(req: SignoutRequest):
    assert req.signout_time is not None
    assert len(req.np_worksession) > 0


class TestGenerateVisitForUser(unittest.TestCase):
    def test_generate_visit_for_user(self):
        api_client = Mock()
        api_client.create_visit_for.side_effect = create_fake_visit
        api_client.get_projects_for.return_value = []
        api_client.get_projects.return_value = []
        api_client.signout.side_effect = fake_signout

        user = User(1, dt.datetime(2022, 1, 1), "foobar", UserType.Student)
        eq = Equipment(1, "something")
        mat = Material(1, "some-material", "g")
        script.generate_visit_for_user(api_client, Faker(), [EquipmentAndMaterials(eq, [mat])], user)

        api_client.create_visit_for.assert_called()
        api_client.signout.assert_called()

