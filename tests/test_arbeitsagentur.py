from datetime import date

from jobby.models import Job
from jobby.sources.arbeitsagentur import _map_to_job

# Ein vollständiges Suchergebnis mit allen Feldern
FULL_ITEM = {
    "stellenangebotsTitel": "Software-Architect (m/w/d)",
    "firma": "adorsys GmbH & Co. KG",
    "referenznummer": "13635-d610d5de_JB5278179-S",
    "stellenlokationen": [
        {"adresse": {"plz": "90429", "ort": "Nürnberg, Mittelfranken"}}
    ],
    "datumErsteVeroeffentlichung": "2026-10-21",
    "externeURL": "https://www.jobexport.de/job/5278179.html",
    "homeofficemoeglich": False,
}

# Ein Suchergebnis ohne externe URL und ohne Home-Office-Angabe
ITEM_WITHOUT_OPTIONALS = {
    "stellenangebotsTitel": "Entwicklungsingenieur Embedded Software (m/w/d)",
    "firma": "persona service AG & Co.KG",
    "referenznummer": "12122-981903126-S",
    "stellenlokationen": [
        {"adresse": {"plz": "82538", "ort": "Geretsried"}}
    ],
    "datumErsteVeroeffentlichung": "2026-11-08",
}


def test_map_to_job_returns_job():
    job = _map_to_job(FULL_ITEM)

    assert isinstance(job, Job)


def test_map_to_job_maps_basic_fields():
    job = _map_to_job(FULL_ITEM)

    assert job.ref_nr == "13635-d610d5de_JB5278179-S"
    assert job.titel == "Software-Architect (m/w/d)"
    assert job.unternehmen == "adorsys GmbH & Co. KG"
    assert job.ort == "Nürnberg, Mittelfranken"
    assert job.plz == "90429"
    assert job.url == "https://www.jobexport.de/job/5278179.html"
    assert job.home_office is False


def test_map_to_job_converts_date():
    job = _map_to_job(FULL_ITEM)

    assert job.datum == date(2026, 10, 21)
    assert isinstance(job.datum, date)


def test_map_to_job_without_optional_fields():
    job = _map_to_job(ITEM_WITHOUT_OPTIONALS)

    assert job.url is None
    assert job.home_office is None


def test_map_to_job_without_plz():
    item = {
        **FULL_ITEM,
        "stellenlokationen": [{"adresse": {"ort": "Berlin"}}],
    }

    job = _map_to_job(item)

    assert job.ort == "Berlin"
    assert job.plz is None


def test_map_to_job_has_no_description_yet():
    job = _map_to_job(FULL_ITEM)

    assert job.beschreibung is None
