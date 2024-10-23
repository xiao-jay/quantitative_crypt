import logging
import time
from functools import wraps


def retry(max_retries=5, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.info(f"func {func.__name__} Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            logging.info(f"func {func.__name__} All {max_retries} attempts failed.")
        return wrapper
    return decorator