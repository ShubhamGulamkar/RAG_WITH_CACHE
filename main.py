# from fastapi import (
#     FastAPI
# )

# from api.upload import (
#     router as upload_router
# )

# from api.query import (
#     router as query_router
# )

# from rag.vector_store import (
#     load_vector_store
# )

# app = FastAPI(
#     title="RAG API"
# )

# load_vector_store()

# app.include_router(
#     upload_router
# )

# app.include_router(
#     query_router
# )

print("STEP A")

from fastapi import FastAPI

print("STEP B")

from api.upload import router as upload_router

print("STEP C")

from api.query import router as query_router

print("STEP D")

from rag.vector_store import load_vector_store

print("STEP E")

app = FastAPI(
    title="RAG API"
)

print("STEP F")

try:
    load_vector_store()
    print("STEP G - Vector Store Loaded")
except Exception as e:
    print(f"VECTOR STORE ERROR: {e}")

print("STEP H")

app.include_router(upload_router)

print("STEP I")

app.include_router(query_router)

print("STEP J")