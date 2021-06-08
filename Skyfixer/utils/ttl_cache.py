from functools import lru_cache, wraps
from time import time
from typing import Optional


def get_ttl_hash(seconds: int):
    return time() // seconds


def ttl_cache(maxsize: Optional[int] = 128, typed: Optional[bool] = False, lifespan: Optional[int] = 300):
    """
    Adds ability to expire for lru_cache.

    :param maxsize: maximum cached calls.
    :param typed: represents if args must be compared by value or type and value.
    :param lifespan: how long cached result will live before being invalidated.
    :return: anything.
    """
    def decorate_cached_function(f):
        @wraps(f)
        def internal_caching(*_args, **_kwargs):
            ttl_hash = get_ttl_hash(lifespan)

            @lru_cache(maxsize, typed)
            def timed_function(*args, _ttl_hash, **kwargs):
                del _ttl_hash
                return f(*args, **kwargs)

            return timed_function(*_args, **_kwargs, _ttl_hash=ttl_hash)
        return internal_caching
    return decorate_cached_function
