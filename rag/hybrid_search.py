# from rank_bm25 import BM25Okapi
# import numpy as np

# import rag.vector_store as vector_store
# from rag.embeddings import (
#     get_embedding_model
# )


# def hybrid_search(
#     question,
#     top_k=10
# ):
#     model = get_embedding_model()

#     query_embedding = (
#         model.encode(
#             [question]
#         )
#     )

#     query_embedding = (
#         np.array(
#             query_embedding
#         ).astype("float32")
#     )

#     distances, ids = (
#         vector_store.index.search(
#             query_embedding,
#             top_k
#         )
#     )

#     semantic_docs = []

#     for idx in ids[0]:

#         if (
#             idx >= 0
#             and idx <
#             len(
#                 vector_store.documents
#             )
#         ):

#             semantic_docs.append(
#                 vector_store.documents[idx]
#             )

#     tokenized_docs = [
#         doc.lower().split()
#         for doc
#         in vector_store.documents
#     ]

#     bm25 = BM25Okapi(
#         tokenized_docs
#     )

#     keyword_scores = (
#         bm25.get_scores(
#             question.lower().split()
#         )
#     )

#     keyword_indices = (
#         np.argsort(
#             keyword_scores
#         )[::-1][:top_k]
#     )

#     keyword_docs = [
#         vector_store.documents[i]
#         for i
#         in keyword_indices
#     ]

#     merged_docs = (
#         semantic_docs
#         + keyword_docs
#     )

#     unique_docs = list(
#         dict.fromkeys(
#             merged_docs
#         )
#     )

#     return unique_docs

from rank_bm25 import BM25Okapi
import numpy as np

import rag.vector_store as vector_store
from rag.embeddings import get_embedding_model


def hybrid_search(
    question,
    top_k=10
):

    print("\n" + "=" * 70)
    print("HYBRID SEARCH STARTED")
    print("=" * 70)

    print(f"Question: {question}")

    model = get_embedding_model()

    print("Generating Query Embedding...")

    query_embedding = model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding
    ).astype(
        "float32"
    )

    print("Running FAISS Search...")

    distances, ids = (
        vector_store.index.search(
            query_embedding,
            top_k
        )
    )

    semantic_docs = []

    print("\nSemantic Search Results")

    for idx in ids[0]:

        if (
            idx >= 0
            and idx <
            len(vector_store.documents)
        ):

            print(
                f"Semantic Chunk Index: {idx}"
            )

            semantic_docs.append(
                vector_store.documents[idx]
            )

    print(
        f"Semantic Chunks Found: "
        f"{len(semantic_docs)}"
    )

    print("\nRunning BM25 Search...")

    tokenized_docs = [
        doc.lower().split()
        for doc in vector_store.documents
    ]

    bm25 = BM25Okapi(
        tokenized_docs
    )

    keyword_scores = bm25.get_scores(
        question.lower().split()
    )

    keyword_indices = (
        np.argsort(
            keyword_scores
        )[::-1][:top_k]
    )

    keyword_docs = []

    print("\nBM25 Results")

    for idx in keyword_indices:

        print(
            f"BM25 Chunk Index: {idx}"
        )

        keyword_docs.append(
            vector_store.documents[idx]
        )

    print(
        f"Keyword Chunks Found: "
        f"{len(keyword_docs)}"
    )

    merged_docs = (
        semantic_docs +
        keyword_docs
    )

    unique_docs = list(
        dict.fromkeys(
            merged_docs
        )
    )

    print(
        f"\nMerged Results: "
        f"{len(unique_docs)}"
    )

    print("=" * 70)

    return unique_docs