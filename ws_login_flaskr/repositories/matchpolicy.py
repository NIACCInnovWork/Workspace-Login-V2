
_check_visits_query = """
    SELECT * FROM visits 
    WHERE visits.user_id=users.user_id 
        AND end_time is NULL
"""

class UserMatchPolicy:
    def __init__(self, users_sql: str):
        self.users_sql = users_sql
        self.bind_vars = []

    @staticmethod
    def ALL() -> 'UserMatchPolicy':
        return UserMatchPolicy("")


    @staticmethod
    def ONGOING() -> 'UserMatchPolicy':
        return UserMatchPolicy(f" AND EXISTS ({_check_visits_query})")

    @staticmethod
    def NOT_ONGOING() -> 'UserMatchPolicy':
        return UserMatchPolicy(f" AND NOT EXISTS ({_check_visits_query})")

    def with_name(self, name: str) -> 'UserMatchPolicy':
        """ Requires the set of user records returned to have a name matching 
        the provided string exactly.

        This functionality is currently used as a means of checking if a user 
        with this name already exists within the system.  This requires an 
        exact match instead of using a match supporting a more fuzzy matching 
        strategy.

        :param:name: The name which must be matched
        :return: A policy with all of the previous matches + the 
        name_constraint policy
        """
        self.users_sql += f" AND name = %s"
        self.bind_vars.append(name)
        return self

class VisitMatchPolicy:
    def __init__(self, visit_sql: str = ""):
        self.visits_sql = visit_sql

    def ALL() -> 'MatchPolicy':
        return VisitMatchPolicy("")

    def ONGOING() -> 'MatchPolicy':
        return VisitMatchPolicy(" AND end_time IS NULL")

    def NOT_ONGOING() -> 'MatchPolicy':
        return VisitMatchPolicy(" AND end_time IS NOT NULL")
