"""
NIACC Innovation Workspace Login V2
This file defines the 'User' class and the associate 'User_Type' enum.
Author: Anthony Riesen
"""

from enum import Enum
import datetime as dt
from typing import List
from dataclasses import dataclass

class UserType(Enum):
    """
    A user (visitor) will be one of several categories of users. This enum lists out these
    options
    """
    Student = 1
    Staff = 2
    Entrepreneur = 3
    Business_Member = 4
    Community_Member = 5

@dataclass
class User:
    """
    A User (visitor) is someone who comes to the makerspace in order to work on projects.

    A user has name and other identifying information, a type, and a date joined.
    """
    user_id: int
    date_joined: dt.datetime
    name: str
    user_type: UserType

@dataclass
class UserSummary:
    id: int
    name: str

