from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Job:
    ref_nr : str
    titel: str
    unternehmen: str
    ort: str
    plz: Optional
    datum: date
    beschreibung: Optional = None
    url: Optional = None
    home_office: Optional = None
