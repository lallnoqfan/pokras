from functools import wraps
from time import perf_counter

from config import AppConfig


def time_performance(func):
    if AppConfig.DEBUG:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = perf_counter()
            result = func(*args, **kwargs)
            end_time = perf_counter()
            execution_time = end_time - start_time
            print('=' * 50)
            print(f"Переданные аргументы: {args}")
            print(f"{func.__name__} выполнилась за {execution_time:.4f} с.")
            print('=' * 50)
            return result

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

    return wrapper


def time_async(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = await coro(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper
