#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""


import redis
import requests
from functools import wraps

# Create a Redis connection
r = redis.Redis()

def url_access_count(method):
    """Decorator for the get_page function"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")
        
        # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)
        
        r.incr(key_count)
        r.set(key, html_content, ex=10)
        return html_content
    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    results = requests.get(url)
    return results.text

if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com'))
