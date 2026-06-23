import json

from cache.redis_client import (
    redis_client
)

CACHE_TTL = 86400


def get_exact_cache(
    question: str
):

    cache = redis_client.get(
        question
    )

    if cache:

        print(
            "[EXACT CACHE HIT]"
        )

        return json.loads(
            cache
        )

    print(
        "[EXACT CACHE MISS]"
    )

    return None


def save_exact_cache(
    question,
    answer
):

    redis_client.setex(
        question,
        CACHE_TTL,
        json.dumps(answer)
    )

    print(
        "[EXACT CACHE SAVED]"
    )