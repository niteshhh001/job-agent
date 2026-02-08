def score_job(job, preferences):
    score = 0

    # Role match (40)
    job_role = job["normalized_title"].lower()
    if any(role in job_role for role in preferences.roles):
        score += 40

    # Location match (30)
    job_location = job["location"].lower()
    if any(loc in job_location for loc in preferences.locations):
        score += 30

    # Skill match (30)
    job_title = job["title"].lower()
    matched_skills = sum(
        1 for skill in preferences.skills if skill in job_title
    )
    if preferences.skills:
        score += (matched_skills / len(preferences.skills)) * 30

    return round(score, 2)
