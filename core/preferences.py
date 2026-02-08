class UserPreferences:
    def __init__(
        self,
        roles,
        locations,
        min_experience=None,
        max_experience=None,
        salary_min=None,
        salary_max=None,
        skills=None
    ):
        self.roles = [r.lower() for r in roles]
        self.locations = [l.lower() for l in locations]
        self.min_experience = min_experience
        self.max_experience = max_experience
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.skills = [s.lower() for s in (skills or [])]
