import unittest
import datetime as dt

from ws_login_domain import Visit

class TestVisit(unittest.TestCase):
    def test_visit_cannot_be_initialized_with_invalid_dates(self):
        with self.assertRaises(ValueError):
            visit = Visit(1, 1, dt.datetime(2022, 5, 5), dt.datetime(2022, 1, 1))

    def test_visit_cannot_set_end_prior_to_start(self):
        visit = Visit(1, 1, dt.datetime(2022, 5, 5), None)

        with self.assertRaises(ValueError):
            visit.end_time = dt.datetime(2022, 1, 1)

    def test_visit_cannot_set_start_after_end(self):
        visit = Visit(1, 1, dt.datetime(2022, 1, 1), dt.datetime(2022, 2, 2))

        with self.assertRaises(ValueError):
            visit.start_time = dt.datetime(2022, 5, 5)


