import requests

def scrape_workday(endpoint, company, max_pages=5, debug=False):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    all_jobs = []
    offset = 0
    limit = 50

    for page in range(max_pages):
        payload = {
            "appliedFacets": {
                "locationHierarchy2": []
            },
            "searchText": "",
            "limit": limit,
            "offset": offset
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            print(f"[Workday] {company} failed ({response.status_code})")
            if debug:
                print(response.text)
            break

        data = response.json()

        if debug and page == 0:
            print(f"[DEBUG] Workday keys for {company}: {list(data.keys())}")

        postings = (
            data.get("jobPostings")
            or data.get("items")
            or data.get("searchResults")
            or data.get("data", {}).get("jobPostings")
            or []
        )

        if not postings:
            break

        for job in postings:
            title = (
                job.get("title")
                or job.get("jobTitle")
                or job.get("titleText")
            )

            location = (
                job.get("locationsText")
                or job.get("location")
                or "Unknown"
            )

            apply_url = (
                job.get("externalPath")
                or job.get("applyUrl")
                or job.get("url")
            )

            if not title or not apply_url:
                continue

            all_jobs.append({
                "company": company,
                "title": title,
                "location": location,
                "apply_url": apply_url,
                "source": "workday"
            })

        offset += limit

    return all_jobs
