# decorators.py
import functools
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

def catch_exceptions(func):
    import traceback
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {func.__name__}: {e}")
            traceback.print_exc()
            return None
    return wrapper
