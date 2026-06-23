# from langchain.text_splitter import (
#     RecursiveCharacterTextSplitter
# )
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

splitter = (
    RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
)


def chunk_text(text):

    return splitter.split_text(
        text
    )