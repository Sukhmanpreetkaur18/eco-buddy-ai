"""
Multi-Layer Caching System for Analytics Endpoints
Purpose: Reduce computation time by caching frequently accessed data.
"""

import time
import logging
from typing import Any, Dict, Callable, Optional

logger = logging.getLogger(__name__)


class TTLCache:
    """
    A simple thread-safe Time-To-Live (TTL) cache.
    """

    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cache_store: Dict[str, tuple] = {}

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value if it exists and has not expired."""
        if key in self.cache_store:
            timestamp, value = self.cache_store[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            else:
                del self.cache_store[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Stores a value with a timestamp."""
        self.cache_store[key] = (time.time(), value)

    def delete(self, key: str) -> bool:
        """Deletes a key from the cache."""
        if key in self.cache_store:
            del self.cache_store[key]
            return True
        return False

    def clear(self) -> None:
        """Clears the entire cache."""
        self.cache_store.clear()

    def get_stats(self) -> Dict[str, int]:
        """Returns cache statistics."""
        return {
            "size": len(self.cache_store),
            "ttl_seconds": self.ttl_seconds,
        }


def cached(ttl_seconds: int = 300):
    """
    Decorator that caches function results based on arguments.
    """
    cache = TTLCache(ttl_seconds=ttl_seconds)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator