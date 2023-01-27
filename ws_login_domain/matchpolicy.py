
class MatchPolicy:
    def __init__(self, users_sql: str, visits_sql: str):
        self.users_sql = users_sql 
        self.visits_sql = visits_sql 
    
    def with_name(self, name) -> 'MatchPolicy':
        # TODO!!! This is really vulnerable to sql injection!!!!
        return MatchPolicy(self.users_sql + f" AND name = '{name}'", self.visits_sql)

    @staticmethod
    def ALL():
        return MatchPolicy("", "")

    def ONGOING():
        return MatchPolicy(
                " AND EXISTS (SELECT * FROM visits WHERE end_time IS NULL AND users.user_id = visits.user_id)",
                " AND end_time IS NULL "
            )

    def NOT_ONGOING():
        return MatchPolicy(
                " AND NOT EXISTS (SELECT * FROM visits WHERE end_time IS NULL AND users.user_id = visits.user_id)",
                " AND end_time IS NOT NULL "
            )
