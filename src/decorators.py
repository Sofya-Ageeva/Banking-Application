from datetime import datetime
from functools import wraps


def log(filename = None):
    """Выводит результат выполнения функции в файл, если такое значение задано по умолчанию"""
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            formatted_time = datetime.now()
            start_time = formatted_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = formatted_time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                success_message = (f"{start_time}\n{func.__name__} ok "
                           f"Результат: {result}"
                                   f"\n{end_time}")

                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(success_message)
                else:
                    print(f"{func.__name__} ok Результат: {result}")
                return result
            except Exception as e:
                error_message = (f"{start_time}\n{func.__name__} "
                                 f"error: {type(e).__name__}."
                                 f"Inputs: {args}, {kwargs}"
                                 f"\n{end_time}")
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(error_message)
                else:
                    print(f"{func.__name__} error: {type(e).__name__}."
                      f"Inputs: {args}, {kwargs}")

                raise
        return inner
    return wrapper
