def extract_job_features(job):
    title = job["normalized_title"].lower()

    features = {
        "role": title,
        "is_backend": "backend" in title,
        "is_frontend": "frontend" in title,
        "is_fullstack": "full stack" in title,
        "is_ml": "ml" in title or "machine learning" in title,
        "is_data": "data" in title
    }

    return features
