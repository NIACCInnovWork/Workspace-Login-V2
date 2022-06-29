"""
NIACC Innovation Workspace Login V2
Integration test file that tests wheather a visit can be added to and loaded from the database.
Author: Anthony Riesen
"""
import datetime
import unittest

from database.class_visit import Visit
from database.initialize_database import start_workspace_database


class TestVisitClass(unittest.TestCase):

    def test_create_visit(self):
        """
        Creates a visit with the current time in the database and loads the visit back to check
        functionality
        :return: test success or failure
        """
        database = start_workspace_database()
        user_id = 1
        visit = Visit.create(database, user_id)

        self.assertIsNotNone(visit.visit_id)
        self.assertIsNotNone(visit.user_id)
        self.assertIsNotNone(visit.start_time)


if __name__ == '__main__':
    unittest.main()
