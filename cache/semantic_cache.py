import pickle
import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from rag.embeddings import (
    get_embedding_model
)

from cache.redis_client import (
    redis_client
)

SIMILARITY_THRESHOLD = 0.90

def save_semantic_cache(
    question,
    answer
):

    model = (
        get_embedding_model()
    )

    embedding = (
        model.encode(question)
    )

    key = (
        f"semantic:{question}"
    )

    redis_client.set(
        key,
        pickle.dumps(
            {
                "embedding": embedding,
                "answer": answer
            }
        )
    )

    print(
        "[SEMANTIC CACHE SAVED]"
    )

def get_semantic_cache(
    question
):

    model = (
        get_embedding_model()
    )

    query_embedding = (
        model.encode(question)
    )

    for key in redis_client.keys(
        "semantic:*"
    ):

        data = pickle.loads(
            redis_client.get(key)
        )

        similarity = (
            cosine_similarity(
                [query_embedding],
                [data["embedding"]]
            )[0][0]
        )

        print(
            f"Similarity : "
            f"{similarity}"
        )

        if similarity >= (
            SIMILARITY_THRESHOLD
        ):

            print(
                "[SEMANTIC CACHE HIT]"
            )

            return (
                data["answer"]
            )

    print(
        "[SEMANTIC CACHE MISS]"
    )

    return None
