#!/usr/bin/env python3
"""Redis Cache class"""

import redis
import uuid
from typing import Union


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
