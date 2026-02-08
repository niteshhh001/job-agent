import json
from core.preferences import UserPreferences
from core.scorer import score_job

with open("data/normalized_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# Example user preferences
user_prefs = UserPreferences(
    roles=["software engineer", "backend engineer"],
    locations=["bangalore", "remote"],
    skills=["python", "api", "backend"]
)

scored_jobs = []

for job in jobs:
    score = score_job(job, user_prefs)
    if score > 0:
        job["match_score"] = score
        scored_jobs.append(job)

# Sort by relevance
scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)

with open("data/matched_jobs.json", "w", encoding="utf-8") as f:
    json.dump(scored_jobs[:50], f, indent=2)

print(f"Total matched jobs: {len(scored_jobs)}")
print("Top match score:", scored_jobs[0]["match_score"] if scored_jobs else "N/A")
