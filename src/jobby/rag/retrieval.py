from jobby.rag.embed import embed_texts
from jobby.rag.store import get_client, COLLECTION_NAME
from jobby.models import ProfileMatch

def search_profile(query: str, limit: int = 3):
    client = get_client()
    if query:
        query_list = [query]
        job_requirement = embed_texts(query_list, is_query=True)
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query = job_requirement[0].tolist(),
            limit = limit,
            with_payload=True,
        )
        profile_matches = []
        for item in response.points:
            match = ProfileMatch(
                id=item.id,
                score=item.score,
                text=item.payload["text"],
                source=item.payload["source"],
                page=item.payload.get("page"),
            )
            profile_matches.append(match)
        return profile_matches
    else:
        return []


if __name__ == "__main__":
    for m in search_profile("Conformal Prediction und Bayessche Neuronale Netze", limit=20):
        print(round(m.score, 3), m.text.split("\n")[1][:50])