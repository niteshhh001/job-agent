from scrapers.greenhouse import scrape_greenhouse
from scrapers.lever import scrape_lever
import json
import os
import time


greenhouse_companies = [
    "stripe",
    "airbnb",
    "coinbase",
    "razorpay"
]

lever_companies = [
    "spotify",
    "databricks",
    "figma",
    "robinhood",
    "airtable",
    "notion"
]


all_jobs = []

for company in greenhouse_companies:
    jobs = scrape_greenhouse(company)
    print(f"[Greenhouse] {company}: {len(jobs)}")
    all_jobs.extend(jobs)


for company in lever_companies:
    jobs = scrape_lever(company)
    print(f"[Lever] {company}: {len(jobs)}")
    all_jobs.extend(jobs)
    time.sleep(1.5)  # polite delay


os.makedirs("data", exist_ok=True)

with open("data/raw_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)

print(f"\nTotal jobs collected: {len(all_jobs)}")
