"""
Comprehensive Unit Tests for Multi-Layer Caching System
Tests TTL expiration, decorator behavior, and cache management.
"""

import time
import pytest
from multi_cache import TTLCache, cached


class TestTTLCacheBasic:
    def test_set_and_get(self):
        """Should store and retrieve values."""
        cache = TTLCache(ttl_seconds=60)
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_get_missing_key(self):
        """Should return None for missing keys."""
        cache = TTLCache(ttl_seconds=60)
        assert cache.get("missing") is None

    def test_overwrite_value(self):
        """Should allow overwriting values."""
        cache = TTLCache(ttl_seconds=60)
        cache.set("key", "value1")
        cache.set("key", "value2")
        assert cache.get("key") == "value2"


class TestTTLCacheExpiration:
    def test_value_expires_after_ttl(self):
        """Should return None after TTL expires."""
        cache = TTLCache(ttl_seconds=1)
        cache.set("key", "value")
        time.sleep(1.2)
        assert cache.get("key") is None

    def test_value_removed_after_expiry(self):
        """Should remove expired keys from the store."""
        cache = TTLCache(ttl_seconds=1)
        cache.set("key", "value")
        time.sleep(1.2)
        cache.get("key")
        assert "key" not in cache.cache_store


class TestTTLCacheManagement:
    def test_delete_key(self):
        """Should delete a specific key."""
        cache = TTLCache(ttl_seconds=60)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.delete("key1") is True
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    def test_delete_missing_key(self):
        """Should return False when deleting a missing key."""
        cache = TTLCache(ttl_seconds=60)
        assert cache.delete("missing") is False

    def test_clear_cache(self):
        """Should clear the entire cache."""
        cache = TTLCache(ttl_seconds=60)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestTTLCacheStats:
    def test_get_stats_size(self):
        """Should return the correct size."""
        cache = TTLCache(ttl_seconds=60)
        cache.set("key1", "value1")
        assert cache.get_stats()["size"] == 1


class TestCachedDecorator:
    def test_function_called_once(self):
        """Should only call the function once when using cache."""
        call_count = 0

        @cached(ttl_seconds=60)
        def my_function():
            nonlocal call_count
            call_count += 1
            return call_count

        assert my_function() == 1
        assert my_function() == 1
        assert call_count == 1

    def test_function_called_again_after_expiry(self):
        """Should call the function again after TTL expires."""
        call_count = 0

        @cached(ttl_seconds=1)
        def my_function():
            nonlocal call_count
            call_count += 1
            return call_count

        assert my_function() == 1
        time.sleep(1.2)
        assert my_function() == 2
        assert call_count == 2

    def test_decorator_works_with_arguments(self):
        """Should cache based on arguments."""
        call_count = 0

        @cached(ttl_seconds=60)
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3
        assert add(2, 3) == 5
        assert call_count == 2