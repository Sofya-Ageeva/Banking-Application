from io import StringIO
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from main import main


@patch('main.open_json_file')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_file_format_selection_json(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_open_json: MagicMock) -> None:
    """Проверка выбора JSON-файла и базовой загрузки"""
    # Настраиваем моки
    mock_path_exists.return_value = True
    mock_open_json.return_value = [{'state': 'EXECUTED', 'description': 'Тестовая операция'}]
    mock_input.side_effect = [
        '1', 'test.json',  # выбор и путь
        'EXECUTED',  # статус
        'Нет',  # сортировка по дате
        'Нет',  # рублёвые
        'Нет'  # поиск по описанию
    ]

    main()
    output = mock_stdout.getvalue()

    assert "Для обработки выбран JSON-файл." in output
    assert "Операции отфильтрованы по статусу \"EXECUTED\"" in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Тестовая операция" in output


@patch('main.read_transaction_from_csv')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_file_format_selection_csv(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_read_csv: MagicMock) -> None:
    """Проверка выбора CSV-файла"""
    mock_path_exists.return_value = True
    mock_read_csv.return_value = [{'state': 'EXECUTED', 'description': 'CSV операция'}]
    mock_input.side_effect = [
        '2', 'test.csv',
        'EXECUTED',
        'Нет',
        'Нет',
        'Нет'
    ]

    main()
    output = mock_stdout.getvalue()

    assert "Для обработки выбран CSV-файл." in output
    assert "Ошибка при загрузке файла" not in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "CSV операция" in output


@patch('main.read_transaction_from_excel')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_file_format_selection_xlsx(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_read_excel: MagicMock) -> None:
    """Проверка выбора XLSX-файла"""
    mock_path_exists.return_value = True
    mock_read_excel.return_value = [{'state': 'EXECUTED', 'description': 'Excel операция'}]
    mock_input.side_effect = [
        '3', 'test.xlsx',
        'EXECUTED',
        'Нет',
        'Нет',
        'Нет'
    ]

    main()
    output = mock_stdout.getvalue()

    assert "Для обработки выбран XLSX-файл." in output
    assert "Ошибка при загрузке файла" not in output
    assert "Всего банковских операций в выборке: 1" in output
    assert "Excel операция" in output


@patch('main.open_json_file')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_date_sorting_ascending(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_open_json: MagicMock) -> None:
    """Проверка сортировки по дате по возрастанию"""
    test_data: List[Dict[str, Any]] = [
        {'state': 'EXECUTED', 'date': '2023-01-03T12:00:00', 'description': 'Третья'},
        {'state': 'EXECUTED', 'date': '2023-01-01T12:00:00', 'description': 'Первая'},
        {'state': 'EXECUTED', 'date': '2023-01-02T12:00:00', 'description': 'Вторая'}
    ]
    mock_path_exists.return_value = True
    mock_open_json.return_value = test_data
    mock_input.side_effect = [
        '1', 'test.json',
        'EXECUTED',
        'Да', 'по возрастанию',  # сортировка
        'Нет',  # рублёвые
        'Нет'   # поиск
    ]

    main()
    output = mock_stdout.getvalue()

    # Ищем строки с описанием
    lines = output.splitlines()
    descriptions_in_output = []
    for line in lines:
        if any(desc in line for desc in ['Первая', 'Вторая', 'Третья']):
            descriptions_in_output.append(line.strip())

    assert len(descriptions_in_output) == 3
    # Проверяем порядок: Первая → Вторая → Третья
    assert 'Первая' in descriptions_in_output[0]
    assert 'Вторая' in descriptions_in_output[1]
    assert 'Третья' in descriptions_in_output[2]


@patch('main.open_json_file')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_ruble_filtering(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_open_json: MagicMock) -> None:
    """Проверка фильтрации только рублевых транзакций"""
    test_data: List[Dict[str, Any]] = [
        {
            'state': 'EXECUTED',
            'operationAmount': {
                'amount': '1000.00',
                'currency': {'name': 'RUB'}
            },
            'description': 'Рублёвая операция'
        },
        {
            'state': 'EXECUTED',
            'operationAmount': {
                'amount': '50.00',
                'currency': {'name': 'USD'}
            },
            'description': 'Долларовая операция'
        }
    ]
    mock_path_exists.return_value = True
    mock_open_json.return_value = test_data
    mock_input.side_effect = [
        '1', 'test.json',
        'EXECUTED',
        'Нет',
        'Да',  # только рублёвые
        'Нет'   # поиск
    ]

    main()
    output = mock_stdout.getvalue()

    # Основные проверки результата
    assert "Для обработки выбран JSON-файл." in output
    assert "Операции отфильтрованы по статусу \"EXECUTED\"" in output

    # Ключевая проверка: должна остаться только 1 RUB‑операция
    assert "Всего банковских операций в выборке: 1" in output

    # Проверка присутствия рублёвой операции в выводе
    assert "Рублёвая операция" in output
    assert "1000.00 RUB" in output

    # Проверка отсутствия долларовой операции
    usd_lines = [line for line in output.splitlines() if 'Долларовая операция' in line]
    assert len(usd_lines) == 0

    # Дополнительная проверка: убедимся, что USD не упоминается
    usd_mentions = [line for line in output.splitlines() if 'USD' in line]
    assert len(usd_mentions) == 0


@patch('main.open_json_file')
@patch('os.path.exists')
@patch('builtins.input')
@patch('sys.stdout', new_callable=StringIO)
def test_invalid_status_handling(
        mock_stdout: StringIO,
        mock_input: MagicMock,
        mock_path_exists: MagicMock,
        mock_open_json: MagicMock) -> None:
    """Проверка обработки некорректного статуса с повторным запросом"""
    test_data: List[Dict[str, Any]] = [{'state': 'EXECUTED'}]
    mock_path_exists.return_value = True
    mock_open_json.return_value = test_data
    mock_input.side_effect = [
        '1', 'test.json',
        'INVALID_STATUS',  # неверный статус
        'EXECUTED',       # корректный статус
        'Нет', 'Нет', 'Нет'  # остальные ответы
    ]

    main()
    output = mock_stdout.getvalue()
    assert "Статус операции \"INVALID_STATUS\" недоступен. Попробуйте ещё раз:" in output
