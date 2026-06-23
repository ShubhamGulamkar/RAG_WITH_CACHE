import faiss
import pickle
import os
import numpy as np

from rag.embeddings import (
    get_embedding_model
)

INDEX_PATH = (
    "data/faiss/index.faiss"
)

DOC_PATH = (
    "data/faiss/docs.pkl"
)

dimension = 384

documents = []

index = faiss.IndexFlatL2(
    dimension
)
def add_documents(chunks):

    global documents

    # embeddings = (
    #     get_embedding_model.encode(
    #         chunks
    #     )
    # )
    model = get_embedding_model()

    embeddings = model.encode(
        chunks
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    index.add(
        embeddings
    )

    documents.extend(
        chunks
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        DOC_PATH,
        "wb"
    ) as f:

        pickle.dump(
            documents,
            f
        )

    print(
        f"{len(chunks)} chunks added"
    )
# def load_vector_store():

#     global index
#     global documents

#     if (
#         os.path.exists(
#             INDEX_PATH
#         )
#     ):

#         index = (
#             faiss.read_index(
#                 INDEX_PATH
#             )
#         )

#         with open(
#             DOC_PATH,
#             "rb"
#         ) as f:

#             documents = (
#                 pickle.load(f)
#             )

#         print(
#             "FAISS Loaded"
#         )
def load_vector_store():

    global index
    global documents

    print("Loading Vector Store")

    if os.path.exists(INDEX_PATH):

        print("Loading FAISS Index")

        index = faiss.read_index(
            INDEX_PATH
        )

        print("Loading Documents")

        with open(
            DOC_PATH,
            "rb"
        ) as f:

            documents = pickle.load(f)

        print(
            f"Loaded {len(documents)} docs"
        )

    else:

        print(
            "No Existing Vector Store"
        )