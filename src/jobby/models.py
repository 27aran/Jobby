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

@dataclass
class Document:
    text: str
    source: str               # Dateiname, z. B. "lebenslauf.pdf"
    page: int | None = None   # Seitenzahl bei PDFs, sonst None

@dataclass
class Chunk:
    text: str
    source: str
    id: str
    page: int | None = None
