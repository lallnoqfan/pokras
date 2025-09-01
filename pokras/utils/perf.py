from functools import wraps
from time import perf_counter

from config import AppConfig


def method_performance(func):
    if not AppConfig.VERBOSE_PERFORMANCE:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('=' * 50)
        print(f"Func: {args[0].__class__.__name__}.{func.__name__}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        print(f"Execution time: {execution_time:.4f}s")
        print('=' * 50)
        return result

    return wrapper


def class_method_performance(func):
    if not AppConfig.VERBOSE_PERFORMANCE:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('=' * 50)
        print(f"Func: {args[0].__name__}.{func.__name__}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        print(f"Execution time: {execution_time:.4f}s")
        print('=' * 50)
        return result

    return wrapper


def function_performance(func):
    if not AppConfig.VERBOSE_PERFORMANCE:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('=' * 50)
        print(f"Func: {func.__name__}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        print(f"Execution time: {execution_time:.4f}s")
        print('=' * 50)
        return result

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


def logtime_async(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = await coro(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('=' * 50)
        print(f"Переданные аргументы: {args}")
        print(f"{coro.__name__} выполнилась за {execution_time:.4f} с.")
        print('=' * 50)
        return result
    return wrapper
