import hashlib

def generate_job_id(company, title, location):
    raw = f"{company}-{title}-{location}".lower()
    return hashlib.md5(raw.encode()).hexdigest()
