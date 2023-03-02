import unittest
from unittest.mock import Mock, call, ANY
import datetime as dt
from faker import Faker
from typing import Optional

from ws_login_domain import User, UserType
from ws_login_scripts.populate_db import UserFactory


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

