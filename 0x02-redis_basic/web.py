#!/usr/bin/env python3
""" A simple caching for getting web page content """
import functools
from typing import Callable

import redis
import requests

store = redis.Redis()


def cache_http_request(func: Callable) -> Callable:
    """Implements caching on a request"""

    @functools.wraps(func)
    def invoker(url):
        # Initialize Redis client
        redis_client = redis.Redis()

        # Retrieve cached HTML content if available
        cached_html = redis_client.get(url)
        if cached_html:
            return cached_html.decode('utf-8')

        # Fetch HTML content using requests
        html_content = func(url)

        # Cache the HTML content with expiration time of 10 seconds
        redis_client.setex(url, 10, html_content)
        # Track the number of accesses to the URL
        count_key = "count:{}".format(url)
        redis_client.incr(count_key)

        return html_content

    return invoker


@cache_http_request
def get_page(url: str) -> str:
    """Retrieves the content of a page"""
    store.set('count:{}'.format(url), 0)
    response = requests.get(url)
    return response.text
