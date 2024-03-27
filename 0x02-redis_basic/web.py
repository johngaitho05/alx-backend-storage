#!/usr/bin/env python3
"""
This module contains get_page function
"""

import redis
from functools import wraps
from typing import Callable

import requests
from requests import get


r = redis.Redis()


def cache_http_request(fxn: Callable) -> Callable:
    """
    Decorator that caches a http request in Redis
    """
    @wraps(fxn)
    def wrapper(url: str) -> str:
        if type(url) != str:
            return ""

        r.incr(f"count:{url}")
        result = r.get(f"{url}")
        if result and type(result) == bytes:
            return result.decode("utf-8")

        result = fxn(url)
        r.setex("{}".format(url), 10, result)
        return result

    return wrapper


@cache_http_request
def get_page(url: str) -> str:
    """
    obtain the HTML content of a particular URL and returns it
    """
    if type(url) != str:
        return ""

    return requests.get(url).text
