# from rag.retriever import (
#     retrieve
# )

# from rag.llm import (
#     generate_answer
# )
# from rag.hybrid_search import (
#     hybrid_search
# )

# from rag.reranker import (
#     rerank
# )

# def ask_question(
#     question
# ):

#     docs = hybrid_search(
#         question
#     )
#     print(
#     f"\nHybrid Search Returned "
#     f"{len(docs)} Chunks"
#     )
#     docs = rerank(
#         question,
#         docs
#     )
#     print(
#     f"\nReranker Returned "
#     f"{len(docs)} Chunks"
#     )

#     context = "\n".join(
#         docs
#     )

#     answer = (
#         generate_answer(
#             question,
#             context
#         )
#     )

#     return {
#         "answer": answer,
#         "source": "llm"
#     }

from cache.exact_cache import (
    get_exact_cache,
    save_exact_cache
)

from cache.semantic_cache import (
    get_semantic_cache,
    save_semantic_cache
)

from rag.hybrid_search import (
    hybrid_search
)

from rag.reranker import (
    rerank
)

from rag.llm import (
    generate_answer
)

from utils.logger import (
    logger
)


def ask_question(
    question: str
):

    print(
        "\n" + "=" * 70
    )
    print(
        "NEW QUESTION RECEIVED"
    )
    print(
        "=" * 70
    )
    print(
        f"Question: {question}"
    )

    logger.info(
        f"Question Received: {question}"
    )

    # ==================================================
    # STEP 1 : EXACT CACHE
    # ==================================================

    print(
        "\nChecking Exact Cache..."
    )

    exact_cache_response = (
        get_exact_cache(
            question
        )
    )

    if exact_cache_response:

        print(
            "EXACT CACHE HIT"
        )

        logger.info(
            "Exact Cache Hit"
        )

        return {
            "answer":
            exact_cache_response,
            "source":
            "exact_cache"
        }

    print(
        "EXACT CACHE MISS"
    )

    # ==================================================
    # STEP 2 : SEMANTIC CACHE
    # ==================================================

    print(
        "\nChecking Semantic Cache..."
    )

    semantic_cache_response = (
        get_semantic_cache(
            question
        )
    )

    if semantic_cache_response:

        print(
            "SEMANTIC CACHE HIT"
        )

        logger.info(
            "Semantic Cache Hit"
        )

        return {
            "answer":
            semantic_cache_response,
            "source":
            "semantic_cache"
        }

    print(
        "SEMANTIC CACHE MISS"
    )

    # ==================================================
    # STEP 3 : HYBRID SEARCH
    # ==================================================

    print(
        "\nRunning Hybrid Search..."
    )

    docs = hybrid_search(
        question
    )

    print(
        f"Hybrid Search Returned "
        f"{len(docs)} Chunks"
    )

    logger.info(
        f"Hybrid Search Returned "
        f"{len(docs)} Chunks"
    )

    # ==================================================
    # STEP 4 : RERANKING
    # ==================================================

    print(
        "\nRunning Cross Encoder Reranker..."
    )

    docs = rerank(
        question,
        docs
    )

    print(
        f"Reranker Returned "
        f"{len(docs)} Chunks"
    )

    logger.info(
        f"Reranker Returned "
        f"{len(docs)} Chunks"
    )

    # ==================================================
    # STEP 5 : CONTEXT CREATION
    # ==================================================

    context = "\n".join(
        docs
    )

    print(
        f"\nContext Length: "
        f"{len(context)}"
    )

    # ==================================================
    # STEP 6 : LLM GENERATION
    # ==================================================

    print(
        "\nCalling LLM..."
    )

    answer = generate_answer(
        question,
        context
    )

    print(
        "LLM Response Generated"
    )

    logger.info(
        "LLM Response Generated"
    )

    # ==================================================
    # STEP 7 : SAVE TO CACHE
    # ==================================================

    print(
        "\nSaving to Exact Cache..."
    )

    save_exact_cache(
        question,
        answer
    )

    print(
        "Saved to Exact Cache"
    )

    print(
        "\nSaving to Semantic Cache..."
    )

    save_semantic_cache(
        question,
        answer
    )

    print(
        "Saved to Semantic Cache"
    )

    logger.info(
        "Response Saved To Cache"
    )

    print(
        "\nReturning Source: llm"
    )

    print(
        "=" * 70
    )

    return {
        "answer": answer,
        "source": "llm"
    }