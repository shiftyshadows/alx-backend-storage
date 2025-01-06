#!/usr/bin/env python3
"""
   This module defines the class: Cache.
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method using Redis."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
       Decorator to store history of inputs and outputs
       of a method in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method and store its output
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    call_count = len(inputs)
    print(f"{method_name} was called {call_count} times:")

    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> "
              f"{output.decode('utf-8')}")


class Cache:
    """
    A class to interact with a Redis database for caching data.

    Methods:
        __init__: Initializes the Redis connection and flushes the database.
        store: Stores data in Redis with a randomly generated key.
        get: Retrieves data from Redis and optionally converts it.
        get_str: Retrieves a string from Redis.
        get_int: Retrieves an integer from Redis.
    """
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and optionally convert it.

        Args:
            key (str): The key to retrieve.
            fn (Optional[Callable]): A function to convert the data.

        Returns:
            Union[str, bytes, int, None]: The retrieved data,
            possibly converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The retrieved string or None if the
            key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[int]: The retrieved integer or None if
            the key does not exist.
        """
        return self.get(key, fn=int)
