#!/usr/bin/env python3
"""Redis Cache class"""

import redis
import uuid
from typing import Union, Callable, Any


class Cache:
    """Redis Cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data to redis and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable) -> Union[Any, None]:
        """Retrieves and converts a value using the passed function"""
        data = self._redis.get(key)
        if not fn:
            return data
        if data:
            return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        """"Retrieves and converts a value to str"""
        data = self._redis.get(key)
        if not data:
            return
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieves and converts a value to int"""
        data = self._redis.get(key)
        if not data:
            return
        return self.get(key, int)
