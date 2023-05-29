""" Provides common authorization utilitys for access to endpoints
"""

import flask
from werkzeug.exceptions import Unauthorized, Forbidden

from typing import List
from flask_login import current_user

class SystemUser:
    """ Represents a user of the login application. 

    This does NOT mean the same as a user of the workspace itself.

    This user must respect the interface established by flask login.
    """
    def __init__(self, id: int, name: str, permissions: List[str], is_authenticated: bool = True):
        self.id = id
        self.name = name
        self.is_authenticated = is_authenticated
        self.is_anonymous = False
        self.is_active = True
        self.permissions = permissions
        
    def get_id(self) -> str:
       return str(self.id)

    def has_permission(self, permission: str) -> bool:
        """ Checks if the user has a specific permission
        """
        return permission in self.permissions

def one_of(*rules):
    """ Joins several auth guards together based on OR logic.
    """
    def inner(func):
        def inner_2(*args, **kwargs):
            for rule in rules:
                try:
                    return rule(func)(*args, **kwargs)
                except (Unauthorized, Forbidden):
                    pass
            flask.abort(403, "Invalid Permissions")
        return inner_2
    return inner


def has_permission(permission: str):
    """ Route guard.

    Ensures only users who are authenticated and have the specified permission
    can invoke the routes guarded by this decorator.
    """
    def inner(func):
        def inner_2(*args, **kwargs):
            if current_user and current_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                flask.abort(403, "Invalid Permissions")
        return inner_2
    return inner

def not_anonymous(func):
    """ Route guard.

    Ensures only sessions which have a user selected may view these routes.  
    This does NOT mean that the user is formally authenticated.  Currenlty, the
    user is not challenged over which user they have selected.
    """
    def inner(*args, **kwargs):
        if current_user and not current_user.is_anonymous:
            return func(*args, **kwargs)
        else:
            flask.abort(403, "Invalid Permissions")
    return inner

# FIXME This is a stupid way to do admin user ids.
admin = SystemUser(-1, 'admin', ['view_stats'], True)
superuser = SystemUser(-2, 'superuser', ['admin', 'view_stats', 'superuser'], True)
