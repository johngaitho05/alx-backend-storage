#!/usr/bin/env python3
"""Redis Cache class"""
import uuid
from functools import wraps
from typing import Union, Callable, Any

import redis

Types = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """ Count Calls """

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ Invokes """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return invoker


class Cache:
    """Redis Cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data to redis and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) \
            -> Union[str, bytes, int, float]:
        """ Get """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """ Get Str """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Get Int """
        return self.get(key, lambda x: int(x))
