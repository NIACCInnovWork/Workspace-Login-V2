import unittest
from ws_login_flaskr.repositories.matchpolicy import UserMatchPolicy, VisitMatchPolicy

class TestUserMatchPolicy(unittest.TestCase):
    def test_user_match_policy_matches_names(self):
        policy = UserMatchPolicy.ALL().with_name("foobar")
        self.assertEqual(" AND name = %s", policy.users_sql)
        self.assertEqual(['foobar'], policy.bind_vars)

class TestVisitMatchPolicy(unittest.TestCase):

    def test_visit_match_policy_generates_sql_matching_policy(self):
        self.assertEqual("", VisitMatchPolicy.ALL().visits_sql)
        self.assertEqual(" AND end_time IS NULL", VisitMatchPolicy.ONGOING().visits_sql)
        self.assertEqual(" AND end_time IS NOT NULL", VisitMatchPolicy.NOT_ONGOING().visits_sql)
