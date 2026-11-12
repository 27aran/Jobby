import sqlite3
from jobby.config import settings
from jobby.sources.arbeitsagentur import search

def _connect():
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)  # data/ anlegen, falls er fehlt
    conn = sqlite3.connect(settings.db_path)
    return conn


def init_db():
    conn = _connect()

    conn.execute("CREATE TABLE IF NOT EXISTS Jobs (id TEXT PRIMARY KEY, titel TEXT, unternehmen TEXT, ort TEXT, plz TEXT, datum TEXT, beschreibung TEXT, url TEXT, home_office INTEGER, status TEXT NOT NULL DEFAULT 'new', gefunden_am TEXT DEFAULT CURRENT_DATE )")

    conn.commit()
    conn.close()

def save_job(job):
    conn = _connect()

    datum = job.datum
    datum = datum.strftime("%Y-%m-%d")

    if job.home_office is True:
        home_office = 1
    elif job.home_office is False:
        home_office = 0
    else:
        home_office = None

    conn.execute("INSERT OR IGNORE INTO Jobs (id, titel, unternehmen, ort, plz, datum, beschreibung, url, home_office) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (job.ref_nr, job.titel, job.unternehmen, job.ort, job.plz, datum, job.beschreibung, job.url, home_office))
    conn.commit()
    conn.close()

def job_exists(ref_nr) -> bool:
    conn = _connect()

    job_id = conn.execute("SELECT id FROM Jobs WHERE id = ?", (ref_nr,)).fetchone()

    conn.close()
    return job_id is not None

if __name__ == "__main__":
    init_db()
    jobs = search("Python", "Stuttgart", published_since= 0, size=5)
    for job in jobs:
        save_job(job)
    print(job_exists(jobs[0].ref_nr))  # True
    print(job_exists("gibts-nicht"))  # False