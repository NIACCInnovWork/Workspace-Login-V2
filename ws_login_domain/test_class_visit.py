import unittest

import datetime as dt
from database.class_visit import Visit

class TestVisit(unittest.TestCase):
    def test_visit_is_ended_if_end_date_is_set(self):
        self.assertTrue(Visit(0, 1, dt.datetime.now(), dt.datetime.now()).is_ended())
        self.assertFalse(Visit(0, 1, dt.datetime.now(), None).is_ended())
