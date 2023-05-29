import unittest
from unittest.mock import patch
import flask
import flask_login
from werkzeug.exceptions import Forbidden
from ws_login_flaskr.permission import one_of, has_permission, SystemUser

app = flask.Flask(__name__)

def is_true(func):
    """ A dummy auth guard which always returns true.
    """
    return func

def is_false(func):
    """ A dummy auth guard which always returns false.
    """
    flask.abort(401)


class TestOneOf(unittest.TestCase):
    def test_if_any_included_check_returns_true_the_whole_returns_true(self):
        @one_of(is_false, is_true)
        def test_function(some_param: str):
            return some_param == "expected"

        self.assertTrue(test_function("expected"))

    def test_if_all_included_check_returns_false_the_whole_returns_false(self):
        @one_of(is_false, is_false)
        def test_function():
            return True

        with self.assertRaises(Forbidden): # Can potentally also raise Unauthorized
            test_function()

class TestHasPermission(unittest.TestCase):
    def test_function_is_executed_if_user_has_permission(self):
        @has_permission("test_permission")
        def test_function(some_param: str):
            return some_param == "expected"
        
        test_user = SystemUser(1, "test_user", ["test_permission"])
        with patch("ws_login_flaskr.permission.current_user", test_user):
            self.assertTrue(test_function("expected"))

    def test_function_is_not_executed_if_user_doesnt_has_permission(self):
        @has_permission("test_permission")
        def test_function():
            return True
        
        test_user = SystemUser(1, "test_user", [])
        with patch("ws_login_flaskr.permission.current_user", test_user):
            with self.assertRaises(Forbidden):
                test_function()

