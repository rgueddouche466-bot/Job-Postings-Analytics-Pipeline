import pandas as pd

def normalize_jobs(data):
    jobs = data.get("results", [])

    records = []
    for job in jobs:
        record = {
            "JOB_ID": str(job.get("id")),
            "TITLE": job.get("title"),
            "COMPANY": job.get("company", {}).get("display_name") if job.get("company") else None,
            "LOCATION": job.get("location", {}).get("display_name") if job.get("location") else None,
            "SALARY_MIN": job.get("salary_min"),
            "SALARY_MAX": job.get("salary_max"),
            "CREATED": job.get("created"),
            "DESCRIPTION": job.get("description"),
        }
        records.append(record)

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["JOB_ID"])
    df = df.reset_index(drop=True)
    return df