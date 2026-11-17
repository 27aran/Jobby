from sentence_transformers import SentenceTransformer
from jobby.config import settings
import time
from functools import lru_cache

@lru_cache
def get_model():
    model_name = settings.embedding_model
    model = SentenceTransformer(model_name)
    return model

def embed_texts(texts: list[str], is_query: bool):
    model = get_model()
    if is_query:
        embeddings = model.encode_query(texts, normalize_embeddings=True)
        return embeddings
    else:
        embeddings = model.encode_document(texts, normalize_embeddings=True)
        return embeddings

if __name__ == "__main__":
    start = time.time()
    get_model()
    print("1. Aufruf:", time.time() - start)

    start = time.time()
    get_model()
    print("2. Aufruf:", time.time() - start)