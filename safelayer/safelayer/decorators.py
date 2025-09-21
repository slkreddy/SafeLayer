from functools import wraps

def apply_guards(manager):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return manager.run(result)
        return wrapper
    return decorator
