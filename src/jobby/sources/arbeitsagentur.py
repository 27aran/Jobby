import requests
import json
from src.jobby.models import Job
import base64
import datetime

BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}

def search(position, location, umkreis=30, size=25, page=1):
    params = {
        "was" : position,
        "wo" : location,
        "umkreis" : umkreis,
        "size" : size,
        "page" : page
    }
    response = requests.get(
        f"{BASE_URL}/pc/v6/jobs",
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    response.raise_for_status()
    json_data = response.json()

    jobs = []
    if json_data.get("ergebnisliste") is not None:
        for item in json_data["ergebnisliste"]:
            jobs.append(_map_to_job(item))
        return jobs
    else:
        print("Currently no jobs")
        return []

def _map_to_job(item: dict) -> Job:
    ref_nr = item["referenznummer"]
    titel = item["stellenangebotsTitel"]
    unternehmen = item["firma"]
    ort = item["stellenlokationen"][0]["adresse"]["ort"]
    plz = item["stellenlokationen"][0].get("plz")

    datum = item["datumErsteVeroeffentlichung"]
    datum_date = datetime.datetime.strptime(datum, "%Y-%m-%d").date()

    url = item.get("externeURL")
    home_office = item.get("homeofficemoeglich")

    job_stelle = Job(
        ref_nr=ref_nr,
        titel=titel,
        unternehmen=unternehmen,
        ort=ort,
        plz=plz,
        datum=datum_date,
        url = url,
        home_office=home_office,
    )
    return job_stelle

def fetch_details(job_stelle):
    ref = job.id
    enc_ref = base64.b64encode(ref)

    response = requests.get(
        f"{BASE_URL}/pc/v4/jobdetails/{enc_ref}",
        headers=HEADERS,
    )


if __name__ == "__main__":
    stellen = []
    jobs = search("werkstudent", "Stuttgart", umkreis=20)
    for job in jobs:
        stellen.append(job)
    print(stellen)