import hashlib
import time


CACHE_TTL_SECONDS = 30 * 60
_cache = {}


def _generate_cache_key(question: str) -> str:

    normalized_question = question.strip().lower()

    return hashlib.sha256(
        normalized_question.encode("utf-8")
    ).hexdigest()


def get_cached_result(question: str):

    cache_key = _generate_cache_key(question)

    cached = _cache.get(cache_key)

    if cached is None:
        return None

    if time.time() >= cached["expires_at"]:

        del _cache[cache_key]

        return None

    return cached


def set_cached_result(
    question: str,
    generated_sql: str,
    result
):
    
    cache_key = _generate_cache_key(question)

    _cache[cache_key] = {
        "question": question,
        "generated_sql": generated_sql,
        "result": result,
        "expires_at": time.time() + CACHE_TTL_SECONDS
    }


def clear_cache():

    _cache.clear()