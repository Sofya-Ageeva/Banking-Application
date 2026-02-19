from typing import Iterator, Optional
import pytest
from datetime import datetime
import os
from src.decorators import log


# Вспомогательная функция для проверки содержимого файла
def read_file_content(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


# Очистка файлов после тестов
@pytest.fixture(autouse=True)
def cleanup_files() -> Iterator[None]:
    yield
    # Удаляем созданные файлы после тестов
    for filename in ['mylog.txt', 'test_output.txt']:
        if os.path.exists(filename):
            os.remove(filename)


class TestLogDecorator:
    def test_success_execution_with_filename(self) -> None:
        """Тест: успешное выполнение с записью в файл"""
        @log(filename="mylog.txt")
        def test_func(x: int, y: int) -> int:
            return x + y

        result = test_func(3, 5)

        # Проверяем результат функции
        assert result == 8

        # Проверяем содержимое файла
        content = read_file_content("mylog.txt")

        # Парсим время из файла (первые строки)
        lines = content.split('\n')
        start_time_str = lines[0]
        func_name_line = lines[1]
        end_time_str = lines[-1]

        # Проверяем формат времени
        datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # Проверяем сообщение функции
        assert "test_func ok Результат: 8" in func_name_line

    def test_success_execution_without_filename(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест: успешное выполнение без filename — вывод в консоль"""
        @log()
        def test_func(x: int) -> int:
            return x * 2

        result = test_func(4)

        # Проверяем результат
        assert result == 8

        # Перехватываем вывод
        captured = capsys.readouterr()

        # Проверяем вывод в консоль
        assert "test_func ok Результат: 8" in captured.out

    def test_exception_with_filename(self) -> None:
        """Тест: исключение с записью в файл"""
        @log(filename="mylog.txt")
        def problematic_func(x: int, y: int) -> float:
            return x / y  # вызовет ZeroDivisionError при y=0

        with pytest.raises(ZeroDivisionError):
            problematic_func(10, 0)

        # Проверяем содержимое файла
        content = read_file_content("mylog.txt")
        lines = content.split('\n')

        start_time_str = lines[0]
        error_line = lines[1]
        end_time_str = lines[-1]

        # Проверяем время
        datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # Проверяем сообщение об ошибке
        assert "problematic_func error: ZeroDivisionError" in error_line
        assert "Inputs: (10, 0), {}" in error_line

    def test_exception_without_filename(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест: исключение без filename — вывод в консоль"""
        @log()
        def problematic_func() -> None:
            raise ValueError("Тестовая ошибка")

        with pytest.raises(ValueError):
            problematic_func()

        # Перехватываем вывод
        captured = capsys.readouterr()

        # Проверяем вывод в консоль
        assert "problematic_func error: ValueError" in captured.out
        assert "Inputs: (), {}" in captured.out

    def test_function_with_args_and_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест: функция с аргументами и kwargs — вывод в консоль"""
        @log()
        def complex_func(a: int, b: int, c: Optional[int] = None) -> int:
            if c:
                return a + b + c
            return a + b

        result1 = complex_func(1, 2)
        result2 = complex_func(1, 2, c=3)

        # Проверяем результаты
        assert result1 == 3
        assert result2 == 6

        # Перехватываем вывод
        captured = capsys.readouterr()

        # Проверяем оба сообщения
        assert "complex_func ok Результат: 3" in captured.out
        assert "complex_func ok Результат: 6" in captured.out

    def test_empty_filename_parameter(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест: filename=None — должен выводить в консоль"""
        @log(filename=None)
        def simple_func() -> str:
            return "OK"

        result = simple_func()

        assert result == "OK"

        captured = capsys.readouterr()
        assert "simple_func ok Результат: OK" in captured.out

    def test_file_overwrite_behavior(self) -> None:
        """Тест: проверка перезаписи файла (режим 'w')"""
        @log(filename="test_output.txt")
        def func1() -> int:
            return 1

        @log(filename="test_output.txt")
        def func2() -> int:
            return 2

        # Вызываем функции последовательно
        func1()
        func2()

        # После второго вызова в файле должен быть только результат func2
        content = read_file_content("test_output.txt")
        assert "func1" not in content  # func1 перезаписан
        assert "func2 ok Результат: 2" in content

    def test_multiple_calls_same_function(self) -> None:
        """Тест: многократный вызов одной функции с записью в файл"""
        @log(filename="mylog.txt")
        def counter(x: int) -> int:
            return x + 1

        counter(1)
        counter(2)

        # Каждый вызов перезаписывает файл — проверяем последний результат
        content = read_file_content("mylog.txt")
        assert "counter ok Результат: 3" in content
        # В файле нет следов первого вызова
        assert "counter ok Результат: 2" not in content
