def normalize_location(location: str) -> str:
    loc = location.lower()

    if "bangalore" in loc or "bengaluru" in loc or "blr" in loc:
        return "Bangalore"
    if "remote" in loc:
        return "Remote"
    if "hyderabad" in loc:
        return "Hyderabad"
    if "delhi" in loc or "gurgaon" in loc:
        return "Delhi NCR"

    return location
