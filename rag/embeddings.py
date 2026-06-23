# from sentence_transformers import (
#     SentenceTransformer
# )

# from config.settings import (
#     EMBEDDING_MODEL
# )

# print(
#     "Loading Embedding Model..."
# )

# embedding_model = (
#     SentenceTransformer(
#         EMBEDDING_MODEL
#     )
# )

# print(
#     "Embedding Model Loaded"
# )

# from sentence_transformers import SentenceTransformer

# print("STEP 1: Starting embeddings.py")

# MODEL_NAME = "all-MiniLM-L6-v2"

# print(f"STEP 2: Loading model {MODEL_NAME}")

# embedding_model = SentenceTransformer(MODEL_NAME)

# print("STEP 3: Model loaded successfully")

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        print("Loading Embedding Model...")
        _embedding_model = SentenceTransformer(
            MODEL_NAME
        )
        print("Embedding Model Loaded")

    return _embedding_model