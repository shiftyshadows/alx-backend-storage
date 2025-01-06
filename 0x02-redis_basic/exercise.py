#!/usr/bin/env python3
"""
   This module defines the class: Cache.
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
           Store data in Redis with a randomly generated key.

           Args:
            data (Union[str, bytes, int, float]): The data to store.

           Returns:
            str: The generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
