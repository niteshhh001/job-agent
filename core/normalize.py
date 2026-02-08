import re

def normalize_title(title: str) -> str:
    title = title.lower()

    if re.search(r"\b(sde|software engineer)\b", title):
        return "Software Engineer"
    if "backend" in title:
        return "Backend Engineer"
    if "frontend" in title:
        return "Frontend Engineer"
    if "full stack" in title:
        return "Full Stack Engineer"
    if "data scientist" in title:
        return "Data Scientist"
    if "machine learning" in title:
        return "ML Engineer"

    return title.title()
