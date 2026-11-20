from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams
from jobby.config import settings
from functools import lru_cache
from jobby.models import Chunk
from jobby.rag.embed import embed_texts
from jobby.rag.ingest import load_documents
from jobby.rag.chunk import chunk_document

COLLECTION_NAME = "profile_chunks"

@lru_cache()
def get_client():
    client = QdrantClient(path=str(settings.qdrant_path))

    if not client.collection_exists(COLLECTION_NAME):

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )
    return client

def index_chunks(chunks: list[Chunk]):
    client = get_client()
    points = []
    chunk_texts = [chunk.text for chunk in chunks]
    embeds = embed_texts(chunk_texts, False)

    for chunk, embed in zip(chunks, embeds):
        points.append(
                models.PointStruct(
                    id=chunk.id,
                    vector=embed.tolist(),
                    payload= {"text": chunk.text,
                              "source": chunk.source,
                              "page": chunk.page
                              }
                )
        )
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

if __name__ == "__main__":
    chunks = []
    for doc in load_documents():
        chunks.extend(chunk_document(doc))

    index_chunks(chunks)
    print("Chunks:", len(chunks))
    print("In Qdrant:", get_client().count(COLLECTION_NAME).count)
    get_client().close()