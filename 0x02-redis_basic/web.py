#!/usr/bin/env python3
"""Web.py"""

import requests
from functools import wraps
from redis import Redis as R
from typing import Callable


def count_url_access(method: Callable) -> Callable:
    """count_url_access: counts
    how many times a url is accessed"""
    @wraps(method)
    def wrapper(url):
        """wrapper"""
        cached_url = f'cached:{url}'
        cached_data = R.get(cached_url)
        if cached_data:
            return cached_data.decode('utf-8')
        count_key = f'count:{url}'
        html_cont = method(url)

        R.incr(count_key)
        R.set(cached_url, html_cont)
        R.expire(cached_url, 10)
        return html_cont
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """get_page: returns
    html content of a given url"""
    resp = requests.get(url)
    return resp.text
