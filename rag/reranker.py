# from sentence_transformers import CrossEncoder

# print("Loading Reranker Model...")

# reranker = CrossEncoder(
#     "cross-encoder/ms-marco-MiniLM-L-6-v2"
# )

# print("Reranker Loaded")


# def rerank(
#     question,
#     documents,
#     top_k=3
# ):
#     pairs = [
#         (question, doc)
#         for doc in documents
#     ]

#     scores = reranker.predict(
#         pairs
#     )

#     ranked = sorted(
#         zip(documents, scores),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return [
#         doc
#         for doc, score
#         in ranked[:top_k]
#     ]

from sentence_transformers import (
    CrossEncoder
)

print(
    "Loading CrossEncoder..."
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

print(
    "CrossEncoder Loaded Successfully"
)


def rerank(
    question,
    documents,
    top_k=3
):

    print("\n" + "=" * 70)
    print("RERANKER STARTED")
    print("=" * 70)

    print(
        f"Documents Received: "
        f"{len(documents)}"
    )

    pairs = [
        (question, doc)
        for doc in documents
    ]

    print(
        "Generating Relevance Scores..."
    )

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    print("\nReranker Scores")

    for i, (
        doc,
        score
    ) in enumerate(ranked):

        print(
            f"\nRank {i+1}"
        )

        print(
            f"Score: {score:.4f}"
        )

        print(
            doc[:200]
        )

    final_docs = [
        doc
        for doc,
        score in ranked[:top_k]
    ]

    print(
        f"\nTop {top_k} Chunks Selected"
    )

    print("=" * 70)

    return final_docs