import json
import os

from utils.hash_utils import (
    generate_file_hash
)
from utils.metadata_store import (
    load_metadata,
    save_metadata
)

from rag.chunker import (
    chunk_text
)
from rag.document_loader import (
    load_document
)
from rag.vector_store import (
    add_documents
)

META_FILE = (
    "metadata/processed_files.json"
)

def load_metadata():

    if not os.path.exists(
        META_FILE
    ):
        return {}

    with open(
        META_FILE,
        "r"
    ) as f:

        return json.load(f)
    
# def process_document(
#     filename,
#     file_bytes
# ):

#     metadata = (
#         load_metadata()
#     )

#     file_hash = (
#         generate_file_hash(
#             file_bytes
#         )
#     )

#     if file_hash in metadata:

#         return (
#             False,
#             "Duplicate file"
#         )

#     text = (
#         file_bytes.decode(
#             "utf-8"
#         )
#     )

#     chunks = chunk_text(
#         text
#     )

#     add_documents(
#         chunks
#     )

#     metadata[
#         file_hash
#     ] = filename

#     with open(
#         META_FILE,
#         "w"
#     ) as f:

#         json.dump(
#             metadata,
#             f,
#             indent=4
#         )

#     return (
#         True,
#         f"{len(chunks)} chunks added"
#     )
def process_document(
    filename,
    file_bytes
):

    metadata = (
        load_metadata()
    )

    file_hash = (
        generate_file_hash(
            file_bytes
        )
    )

    if file_hash in metadata:

        print(
            "Duplicate file found"
        )

        return (
            False,
            "Duplicate file"
        )

    text = load_document(
        filename,
        file_bytes
    )

    chunks = chunk_text(
        text
    )

    add_documents(
        chunks
    )

    metadata[
        file_hash
    ] = filename

    save_metadata(
        metadata
    )

    return (
        True,
        f"{len(chunks)} chunks added"
    )