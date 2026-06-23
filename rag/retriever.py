# import numpy as np

# # from rag.embeddings import (
# #     embedding_model
# # )
# from rag.embeddings import get_embedding_model

# # from rag.vector_store import (
# #     index,
# #     documents
# # )
# import rag.vector_store as vector_store

# def retrieve(
#     question,
#     top_k=3
# ):

#     # query_embedding = (
#     #     get_embedding_model.encode(
#     #         [question]
#     #     )
#     # )
#     model = get_embedding_model()

#     query_embedding = model.encode(
#         [question]
#     )

#     distances, ids = (
#         vector_store.index.search(
#             np.array(
#                 query_embedding
#             ).astype(
#                 "float32"
#             ),
#             top_k
#         )
#     )

#     results = []

#     for idx in ids[0]:

#         if idx < len(
#             documents
#         ):
#             results.append(
#                 vector_store.documents[idx]
#             )

#     return results

import numpy as np

from rag.embeddings import (
    get_embedding_model
)

import rag.vector_store as vector_store


def retrieve(
    question,
    top_k=3
):

    model = get_embedding_model()

    query_embedding = model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding
    ).astype(
        "float32"
    )

    print("=" * 50)

    print(
        f"Documents Count: "
        f"{len(vector_store.documents)}"
    )

    print(
        f"FAISS Count: "
        f"{vector_store.index.ntotal}"
    )

    distances, ids = (
        vector_store.index.search(
            query_embedding,
            top_k
        )
    )

    print(
        f"Retrieved IDs: {ids}"
    )

    results = []

    for idx in ids[0]:

        if idx < 0:
            continue

        if idx >= len(
            vector_store.documents
        ):

            print(
                f"Invalid Index: {idx}"
            )

            continue

        results.append(
            vector_store.documents[idx]
        )

    return results