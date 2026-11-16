import uuid
from jobby.models import Chunk
from jobby.models import Document
from ingest import load_documents

SECTION_HEADINGS = {
    "profil",
    "technische kenntnisse",
    "erfahrung & projekte",
    "ausbildung",
    "sprachen & interessen",
}

custom_namespace = uuid.UUID('8f14e45f-ea9c-4b88-9c3c-7f8a12345678')

def create_chunk_id(text: str, source: str) -> str:
    chunk_id: str = ""
    conc_text = text.join(source)
    chunk_id = str(uuid.uuid5(custom_namespace, conc_text))
    return chunk_id

def _is_heading(line: str) -> bool:
    normalized = line.strip().lower().rstrip(":")
    return normalized in SECTION_HEADINGS

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

    for line in doc.text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if _is_heading(line) and current_lines:
            chunks.append(_make_chunk(current_lines, doc))
            current_lines = []

        current_lines.append(line)

    if current_lines:
        chunks.append(_make_chunk(current_lines, doc))

    return chunks

if __name__ == "__main__":
    for doc in load_documents():
        chunks = chunk_document(doc)
        print(repr(doc.text[:1000]))

    for i, chunk in enumerate(chunks, start=1):
        print(len(chunks))
        print(f"===== Chunk {i} | {chunk.source} | Seite {chunk.page} | {len(chunk.text)} Zeichen =====")
        print(chunk.text)
        print()

