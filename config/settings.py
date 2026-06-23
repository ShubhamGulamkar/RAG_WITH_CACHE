from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL"
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP")
)