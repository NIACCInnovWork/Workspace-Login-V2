import unittest
import datetime as dt

from ws_login_domain import Visit
from ws_login_domain.requests import SignoutRequest

class TestSignoutRequest(unittest.TestCase):
    def test_to_dict_contains_all_req_values(self):
        signout_time = dt.datetime(2022, 1, 1)

        visit = Visit(1, 2, dt.datetime.now(), None)
        signout_request = SignoutRequest.for_visit(visit, signout_time)

        d = signout_request.to_dict()

        self.assertEqual(signout_time.isoformat(), d['signoutTime'])

    def test_fom_dict_deserializes_all_req_values(self):
        signout_time = dt.datetime(2022, 1, 1)
        signout_req = SignoutRequest.from_dict(1, {
            'signoutTime': signout_time.isoformat(),
            'newProjectWorkSessions': [],
            'existingProjectWorkSessions': [],
        })

        self.assertEqual(signout_time, signout_req.signout_time)
