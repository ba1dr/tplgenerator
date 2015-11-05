# -*- coding: utf-8 -*-


def safe_handle_errors_log(logger, fname=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                logger.exception("Function %s error!" % (fname or func.__name__))
                return None
        return inner
    return wrapper
