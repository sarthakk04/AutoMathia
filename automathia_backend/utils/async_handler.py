from functools import wraps
from fastapi import Request
from utils.api_error import APIError

def async_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIError as e:
            raise e
        except Exception as e:
            print(f"❌ [ERROR] {func.__name__}: {e}")
            raise APIError("Internal Server Error", 500)
    return wrapper
