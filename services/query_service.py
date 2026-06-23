from rag.retriever import (
    retrieve
)

from rag.llm import (
    generate_answer
)
from rag.hybrid_search import (
    hybrid_search
)

from rag.reranker import (
    rerank
)

def ask_question(
    question
):

    docs = hybrid_search(
        question
    )
    print(
    f"\nHybrid Search Returned "
    f"{len(docs)} Chunks"
    )
    docs = rerank(
        question,
        docs
    )
    print(
    f"\nReranker Returned "
    f"{len(docs)} Chunks"
    )

    context = "\n".join(
        docs
    )

    answer = (
        generate_answer(
            question,
            context
        )
    )

    return {
        "answer": answer,
        "source": "llm"
    }