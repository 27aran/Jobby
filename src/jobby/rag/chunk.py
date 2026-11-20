import uuid
import re
from jobby.models import Chunk
from jobby.models import Document
from jobby.rag.ingest import load_documents

SECTION_HEADINGS = {
    "profil",
    "technische kenntnisse",
    "erfahrung & projekte",
    "ausbildung",
    "sprachen & interessen",
}

custom_namespace = uuid.UUID('8f14e45f-ea9c-4b88-9c3c-7f8a12345678')

def create_chunk_id(text: str, source: str) -> str:
    conc_text = f"{text}::{source}"
    chunk_id = str(uuid.uuid5(custom_namespace, conc_text))
    return chunk_id

def _is_heading(line: str) -> bool:
    normalized = line.strip().lower().rstrip(":")
    return normalized in SECTION_HEADINGS

def _is_new_project(line: str) -> bool:
    normalized = line.strip().rstrip(":")
    return normalized.endswith("projekt") or normalized.endswith("Projekt")

def _is_new_project_year(line: str) -> bool:
    normalized = line.strip().lower().rstrip(":")
    return re.search(r"\d{4}\Z", normalized) is not None

def _make_chunk(lines: list[str], doc: Document) -> Chunk:
    text = "\n".join(lines)
    return Chunk(
        text=text,
        source=doc.source,
        page=doc.page,
        id=create_chunk_id(source=doc.source, text=text),
    )

def chunk_document(doc: Document) -> list[Chunk]:
    chunks = []
    current_lines = []
    current_heading = None

    for line in doc.text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if _is_heading(line):
            if current_lines:
                chunks.append(_make_chunk(current_lines, doc))
            current_heading = line
            current_lines = [line]
            continue

        if _is_new_project(line) or _is_new_project_year(line):
            only_heading = current_lines == [current_heading]
            if current_lines and not only_heading:
                chunks.append(_make_chunk(current_lines, doc))
                current_lines = [current_heading] if current_heading else []

        current_lines.append(line)

    if current_lines:
        chunks.append(_make_chunk(current_lines, doc))

    return chunks

if __name__ == "__main__":
    for doc in load_documents():
        chunks = chunk_document(doc)
        print(repr(doc.text[:1000]))

    for i, chunk in enumerate(chunks, start=1):
        print(f"===== Chunk {i} | {chunk.source} | Seite {chunk.page} | {len(chunk.text)} Zeichen =====")
        print(chunk.text)
        print()

