#!/usr/bin/env python3
""" A simple caching for getting web page content """
import redis
import requests
from functools import wraps
from typing import Callable


store = redis.Redis()


def request_memo(method: Callable) -> Callable:
    """ Remembers call history """
    @wraps(method)
    def invoker(url) -> str:
        """ Invoker """
        store.incr(f'count:{url}')
        result = store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        store.set(f'count:{url}', 0)
        store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@request_memo
def get_page(url: str) -> str:
    """ Gets the content of a web page """
    return requests.get(url).text
