from time import time
from functools import wraps


def log(filename = None):
    def wrapper(func):
        @wraps(func)
        def inner (*args, **kwargs):
            start_func = time()
            result = func(*args, **kwargs)
            end_time = time()






@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
