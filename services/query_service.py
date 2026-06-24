# from cache.exact_cache import (
#     get_exact_cache,
#     save_exact_cache
# )

# from cache.semantic_cache import (
#     get_semantic_cache,
#     save_semantic_cache
# )

# from rag.hybrid_search import (
#     hybrid_search
# )

# from rag.reranker import (
#     rerank
# )

# from rag.llm import (
#     generate_answer
# )

# from utils.logger import (
#     logger
# )


# def ask_question(
#     question: str
# ):

#     print(
#         "\n" + "=" * 70
#     )
#     print(
#         "NEW QUESTION RECEIVED"
#     )
#     print(
#         "=" * 70
#     )
#     print(
#         f"Question: {question}"
#     )

#     logger.info(
#         f"Question Received: {question}"
#     )

#     # ==================================================
#     # STEP 1 : EXACT CACHE
#     # ==================================================

#     print(
#         "\nChecking Exact Cache..."
#     )

#     exact_cache_response = (
#         get_exact_cache(
#             question
#         )
#     )

#     if exact_cache_response:

#         print(
#             "EXACT CACHE HIT"
#         )

#         logger.info(
#             "Exact Cache Hit"
#         )

#         return {
#             "answer":
#             exact_cache_response,
#             "source":
#             "exact_cache"
#         }

#     print(
#         "EXACT CACHE MISS"
#     )

#     # ==================================================
#     # STEP 2 : SEMANTIC CACHE
#     # ==================================================

#     print(
#         "\nChecking Semantic Cache..."
#     )

#     semantic_cache_response = (
#         get_semantic_cache(
#             question
#         )
#     )

#     if semantic_cache_response:

#         print(
#             "SEMANTIC CACHE HIT"
#         )

#         logger.info(
#             "Semantic Cache Hit"
#         )

#         return {
#             "answer":
#             semantic_cache_response,
#             "source":
#             "semantic_cache"
#         }

#     print(
#         "SEMANTIC CACHE MISS"
#     )

#     # ==================================================
#     # STEP 3 : HYBRID SEARCH
#     # ==================================================

#     print(
#         "\nRunning Hybrid Search..."
#     )

#     docs = hybrid_search(
#         question
#     )

#     print(
#         f"Hybrid Search Returned "
#         f"{len(docs)} Chunks"
#     )

#     logger.info(
#         f"Hybrid Search Returned "
#         f"{len(docs)} Chunks"
#     )

#     # ==================================================
#     # STEP 4 : RERANKING
#     # ==================================================

#     print(
#         "\nRunning Cross Encoder Reranker..."
#     )

#     docs = rerank(
#         question,
#         docs
#     )

#     print(
#         f"Reranker Returned "
#         f"{len(docs)} Chunks"
#     )

#     logger.info(
#         f"Reranker Returned "
#         f"{len(docs)} Chunks"
#     )

#     # ==================================================
#     # STEP 5 : CONTEXT CREATION
#     # ==================================================

#     context = "\n".join(
#         docs
#     )

#     print(
#         f"\nContext Length: "
#         f"{len(context)}"
#     )

#     # ==================================================
#     # STEP 6 : LLM GENERATION
#     # ==================================================

#     print(
#         "\nCalling LLM..."
#     )

#     answer = generate_answer(
#         question,
#         context
#     )

#     print(
#         "LLM Response Generated"
#     )

#     logger.info(
#         "LLM Response Generated"
#     )

#     # ==================================================
#     # STEP 7 : SAVE TO CACHE
#     # ==================================================

#     print(
#         "\nSaving to Exact Cache..."
#     )

#     save_exact_cache(
#         question,
#         answer
#     )

#     print(
#         "Saved to Exact Cache"
#     )

#     print(
#         "\nSaving to Semantic Cache..."
#     )

#     save_semantic_cache(
#         question,
#         answer
#     )

#     print(
#         "Saved to Semantic Cache"
#     )

#     logger.info(
#         "Response Saved To Cache"
#     )

#     print(
#         "\nReturning Source: llm"
#     )

#     print(
#         "=" * 70
#     )

#     return {
#         "answer": answer,
#         "source": "llm"
#     }

from rag.hybrid_search import (
    hybrid_search
)

from rag.reranker import (
    rerank
)

from rag.llm import (
    generate_answer
)

from cache.exact_cache import (
    get_exact_cache,
    save_exact_cache
)

from cache.semantic_cache import (
    get_semantic_cache,
    save_semantic_cache
)

from app_guardrails.guardrail_service import (
    run_guardrails
)

from app_guardrails.output_masker import (
    mask_output
)


def ask_question(question):
    print(
        "\n======================================================================"
    )
    print(
        "NEW QUESTION RECEIVED"
    )
    print(
        "======================================================================"
    )
    print(
        f"Question: {question}"
    )

    # ============================================================
    # PHASE 3 - GUARDRAILS
    # ============================================================
    print(
        "\n[STEP 1] RUNNING GUARDRAILS..."
    )

    is_valid, guardrail_message = (
        run_guardrails(
            question
        )
    )

    if not is_valid:
        print(
            "\nGUARDRAILS BLOCKED THE REQUEST"
        )
        print(
            f"Reason: {guardrail_message}"
        )

        return {
            "answer": guardrail_message,
            "source": "guardrail"
        }

    print(
        "GUARDRAILS PASSED"
    )

    # ============================================================
    # PHASE 2 - EXACT CACHE
    # ============================================================
    print(
        "\n[STEP 2] CHECKING EXACT CACHE..."
    )

    exact_cache_answer = (
        get_exact_cache(
            question
        )
    )

    if exact_cache_answer:
        print(
            "EXACT CACHE HIT"
        )
        print(
            "Returning response from exact cache"
        )

        masked_answer = (
            mask_output(
                exact_cache_answer
            )
        )

        return {
            "answer": masked_answer,
            "source": "exact_cache"
        }

    print(
        "EXACT CACHE MISS"
    )

    # ============================================================
    # PHASE 2 - SEMANTIC CACHE
    # ============================================================
    print(
        "\n[STEP 3] CHECKING SEMANTIC CACHE..."
    )

    semantic_cache_answer = (
        get_semantic_cache(
            question
        )
    )

    if semantic_cache_answer:
        print(
            "SEMANTIC CACHE HIT"
        )
        print(
            "Returning response from semantic cache"
        )

        masked_answer = (
            mask_output(
                semantic_cache_answer
            )
        )

        return {
            "answer": masked_answer,
            "source": "semantic_cache"
        }

    print(
        "SEMANTIC CACHE MISS"
    )

    # ============================================================
    # PHASE 1 - HYBRID SEARCH
    # ============================================================
    print(
        "\n[STEP 4] RUNNING HYBRID SEARCH..."
    )

    docs = hybrid_search(
        question
    )

    if not docs:
        print(
            "No documents returned from hybrid search"
        )

        fallback_answer = (
            "I could not find relevant information in the uploaded documents."
        )

        fallback_answer = (
            mask_output(
                fallback_answer
            )
        )

        return {
            "answer": fallback_answer,
            "source": "llm"
        }

    print(
        f"Hybrid Search Returned {len(docs)} Chunks"
    )

    # ============================================================
    # PHASE 1 - RERANKER
    # ============================================================
    print(
        "\n[STEP 5] RUNNING RERANKER..."
    )

    reranked_docs = (
        rerank(
            question,
            docs
        )
    )

    if not reranked_docs:
        print(
            "Reranker returned no documents, using hybrid docs directly"
        )
        reranked_docs = docs

    print(
        f"Reranker Returned {len(reranked_docs)} Chunks"
    )

    # ============================================================
    # BUILD CONTEXT
    # ============================================================
    print(
        "\n[STEP 6] BUILDING CONTEXT..."
    )

    context = "\n\n".join(
        reranked_docs
    )

    print(
        f"Context Length: {len(context)} characters"
    )

    # ============================================================
    # GENERATE ANSWER
    # ============================================================
    print(
        "\n[STEP 7] GENERATING ANSWER FROM LLM..."
    )

    answer = generate_answer(
        question,
        context
    )

    print(
        "LLM Answer Generated"
    )

    # ============================================================
    # OUTPUT MASKING
    # ============================================================
    print(
        "\n[STEP 8] RUNNING OUTPUT MASKING..."
    )

    answer = mask_output(
        answer
    )

    print(
        "Output Masking Completed"
    )

    # ============================================================
    # SAVE TO CACHES
    # ============================================================
    print(
        "\n[STEP 9] SAVING RESPONSE TO CACHE..."
    )

    try:
        save_exact_cache(
            question,
            answer
        )
        print(
            "Exact Cache Saved"
        )
    except Exception as e:
        print(
            f"Exact Cache Save Failed: {e}"
        )

    try:
        save_semantic_cache(
            question,
            answer
        )
        print(
            "Semantic Cache Saved"
        )
    except Exception as e:
        print(
            f"Semantic Cache Save Failed: {e}"
        )

    print(
        "\n======================================================================"
    )
    print(
        "REQUEST COMPLETED SUCCESSFULLY"
    )
    print(
        "======================================================================"
    )

    return {
        "answer": answer,
        "source": "llm"
    }