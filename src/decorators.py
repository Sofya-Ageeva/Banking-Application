from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[..., Any]:
    """Выводит результат выполнения функции в файл, если такое значение задано по умолчанию"""
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Внутренняя функция декоратора.
            Выполняет логирование до и после вызова декорируемой функции.
            """
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
                    print(error_message)
                raise
        return inner
    return wrapper


if __name__ == "__main__":
    @log(filename="mylog.txt")
    def my_function(x: int, y: int) -> int:
        """Возвращает сумму"""
        return x + y

    my_function("s", 2)
