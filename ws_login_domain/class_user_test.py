"""
NIACC Innovation Workspace Login V2
Integration test file that tests whether a user can be added to and loaded from the database.
Author: Anthony Riesen
"""

import unittest
from random import *

from database.class_user import UserType, User
from database.initialize_database import start_workspace_database


class TestUserClass(unittest.TestCase):

    def test_create_user(self):
        """
        Creates a user with a randomized name in the database and loads the user back to check functionality
        :return: test success or failure
        """
        database = start_workspace_database()
        name = "Anthony Riesen" + " " + str(randint(0, 10000))
        user = User.create(database, name, UserType.Staff.value)

        self.assertIsNotNone(user.user_id)
        self.assertIsNotNone(user.date_joined)
        self.assertEqual(user.name, name)
        self.assertEqual(user.user_type, UserType.Staff)


if __name__ == '__main__':
    unittest.main()

