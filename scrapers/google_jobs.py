from serpapi import GoogleSearch

def scrape_google_jobs(query, api_key, max_results=50):
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "gl": "in",          # country (India)
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = []

    # DEBUG (keep once)
    if "jobs_results" not in results:
        print("[DEBUG] SerpAPI response keys:", results.keys())

    for job in results.get("jobs_results", []):
        jobs.append({
            "company": job.get("company_name", "Unknown"),
            "title": job.get("title"),
            "location": job.get("location", "Unknown"),
            "apply_url": (
                job.get("related_links", [{}])[0].get("link")
                if job.get("related_links") else None
            ),
            "source": "google_jobs"
        })

        if len(jobs) >= max_results:
            break

    return jobs
