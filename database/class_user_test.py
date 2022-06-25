import unittest
from random import *

from database.class_user import UserType, User
from database.initialize_database import start_workspace_database


class TestUserClass(unittest.TestCase):

    def test_create_user(self):
        database = start_workspace_database()
        name = "Anthony Riesen" + " " + str(randint(0, 10000))
        user = User.create(database, name, UserType.Staff.value)
        # print("something")

        self.assertIsNotNone(user.user_id)
        self.assertIsNotNone(user.date_joined)
        self.assertEqual(user.name, name)
        self.assertEqual(user.user_type, UserType.Staff)


if __name__ == '__main__':
    unittest.main()

