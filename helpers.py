from functools import wraps


def authorized():
    def wrapper(a):
        @wraps(a)
        def wrapped(*args, **kwargs):
            if session['signed_in'] != True:
                return error_response()
            return a(*args, **kwargs)
        return wrapped
    return wrapper
