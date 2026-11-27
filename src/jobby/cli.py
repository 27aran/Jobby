import time

from jobby.sources.arbeitsagentur import search, fetch_details
from jobby.storage.db import init_db, save_job, job_exists

def fetch_new_jobs(query, location, umkreis = 25):
    init_db()
    alr_exists_count, saved_count = 0, 0
    jobs = search(query, location, umkreis = umkreis)
    found_count = len(jobs)
    for job in jobs:
        if not job_exists(job.ref_nr):
            try:
                updated_job = fetch_details(job)
                save_job(updated_job)
                saved_count += 1
            except Exception as e:
                print(e, job.ref_nr)
            time.sleep(1)
        else:
            alr_exists_count += 1
            print("Job already exists")
    print(f"Found {found_count} jobs, {alr_exists_count} of them already existed, {saved_count} of them are new")

if __name__ == "__main__":
    fetch_new_jobs("AI Engineer", "Stuttgart", 20)


