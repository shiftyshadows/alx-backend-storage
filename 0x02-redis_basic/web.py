#!/usr/bin/env python3
"""
   This module defines the functions: track_access
   and get_page
"""
import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def track_access(func: Callable) -> Callable:
    """
    Decorator to track access count and cache the
    result of a function.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        # Increment access count
        r.incr(count_key)

        # Check cache
        cached_result = r.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        # Fetch the page and cache the result
        result = func(url)
        r.setex(cache_key, 10, result)
        return result

    return wrapper


@track_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))
