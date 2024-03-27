#!/usr/bin/env python3
"""Redis Cache class"""
import uuid
from functools import wraps
from typing import Union, Callable, Any

import redis

Types = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """ Count The number of times a method is called"""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ Invokes """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return invoker


def call_history(method: Callable) -> Callable:
    """ Remembers Call History """

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ Invoker """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output

    return invoker


def replay(fn: Callable) -> None:
    """ Replay """
    if fn is None or not hasattr(fn, '__self__'):
        return
    fn_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(fn_store, redis.Redis):
        return
    fn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fn_name)
    out_key = '{}:outputs'.format(fn_name)
    fn_calls = 0
    if fn_store.exists(fn_name) != 0:
        fn_calls = int(fn_store.get(fn_name))
    print('{} was called {} times:'.format(fn_name, fn_calls))
    fn_inputs = fn_store.lrange(in_key, 0, -1)
    fn_outputs = fn_store.lrange(out_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print('{}(*{}) -> {}'.format(
            fn_name,
            fn_input.decode("utf-8"),
            fn_output,
        ))


class Cache:
    """Redis Cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
