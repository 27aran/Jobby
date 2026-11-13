from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader
from jobby.config import settings
from jobby.models import Document

SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md"}

def _load_pdf(path: Path) -> list[Document]:
    reader = PdfReader(path)
    documents = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            documents.append(Document(text=text, source=path.name, page=page_number))
    return documents


def _load_text(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    return [Document(text=text, source=path.name)]


def load_documents(folder: Path = settings.profile_dir) -> list[Document]:
    documents = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            documents.extend(_load_pdf(path))
        elif suffix in {".txt", ".md"}:
            documents.extend(_load_text(path))
        else:
            print(f"Übersprungen (Dateityp nicht unterstützt): {path.name}")

    return documents


if __name__ == "__main__":
    for doc in load_documents():
        print(f"=== {doc.source} | Seite {doc.page} | {len(doc.text)} Zeichen ===")
        print(doc.text)
        print()