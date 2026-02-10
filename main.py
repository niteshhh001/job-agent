from scrapers.greenhouse import scrape_greenhouse
from scrapers.lever import scrape_lever
from scrapers.google_jobs import scrape_google_jobs

import json
import os


# =========================
# LOAD SERPAPI KEY CORRECTLY
# =========================
SERP_API_KEY = os.getenv("SERP_API_KEY")

if not SERP_API_KEY:
    raise RuntimeError("❌ SERP_API_KEY environment variable not set")


# =========================
# SOURCES
# =========================
greenhouse_companies = [
    "stripe"
]

lever_companies = [
    "spotify"
]

google_queries = [
    "software engineer in delhi",
    "backend engineer remote",
    "python developer in india",
]


# =========================
# COLLECT JOBS
# =========================
all_jobs = []

# Google Jobs (MAIN SOURCE)
for query in google_queries:
    jobs = scrape_google_jobs(query, SERP_API_KEY)
    print(f"[Google Jobs] {query}: {len(jobs)} jobs")
    all_jobs.extend(jobs)


# =========================
# SAVE OUTPUT
# =========================
os.makedirs("data", exist_ok=True)

with open("data/raw_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)

print(f"\nTotal jobs collected: {len(all_jobs)}")
