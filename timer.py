import functools
import time

def exectime(func, return_result=False):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start=time.perf_counter()
        result = func(*args,**kwargs)
        if return_result:
            return time.perf_counter() - start, result
        return time.perf_counter() - start
    return wrapper
