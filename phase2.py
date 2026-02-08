import json
from core.normalize import normalize_title
from core.location import normalize_location
from core.dedup import generate_job_id

with open("data/raw_jobs.json", "r", encoding="utf-8") as f:
    raw_jobs = json.load(f)

seen = {}
normalized_jobs = []

for job in raw_jobs:
    norm_title = normalize_title(job["title"])
    norm_location = normalize_location(job["location"])
    job_id = generate_job_id(job["company"], norm_title, norm_location)

    if job_id in seen:
        continue

    seen[job_id] = True

    normalized_jobs.append({
        "job_id": job_id,
        "title": job["title"],
        "normalized_title": norm_title,
        "company": job["company"],
        "location": norm_location,
        "apply_url": job["apply_url"],
        "source": job["source"]
    })

with open("data/normalized_jobs.json", "w", encoding="utf-8") as f:
    json.dump(normalized_jobs, f, indent=2)

print(f"Raw jobs: {len(raw_jobs)}")
print(f"Normalized jobs: {len(normalized_jobs)}")
