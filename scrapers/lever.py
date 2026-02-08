import requests
import time

def scrape_lever(company, retries=3):
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=20  # increased timeout
            )

            if response.status_code != 200:
                print(f"[Lever] {company} failed ({response.status_code})")
                return []

            data = response.json()
            jobs = []

            for job in data:
                location = job.get("categories", {}).get("location", "Unknown")

                jobs.append({
                    "company": company,
                    "title": job.get("text"),
                    "location": location,
                    "apply_url": job.get("hostedUrl"),
                    "source": "lever",
                    "job_id": job.get("id")
                })

            return jobs

        except requests.exceptions.ReadTimeout:
            print(f"[Lever] Timeout for {company}, retry {attempt}/{retries}")
            time.sleep(2 * attempt)  # backoff

        except requests.exceptions.RequestException as e:
            print(f"[Lever] Error for {company}: {e}")
            return []

    print(f"[Lever] Giving up on {company}")
    return []
