import requests

def scrape_greenhouse(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"[ERROR] {company} failed ({response.status_code})")
        return []

    data = response.json()
    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "company": company,
            "title": job.get("title"),
            "location": job.get("location", {}).get("name", "Unknown"),
            "apply_url": job.get("absolute_url"),
            "source": "greenhouse",
            "job_id": job.get("id")
        })

    return jobs
