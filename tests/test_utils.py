import json
from typing import Any, Dict, List
from unittest.mock import Mock, mock_open, patch

from src.utils import open_json_file


@patch('os.path.exists', return_value=False)
def test_open_json_not_found(mock_exists: Mock) -> None:
    """Тест: файл не найден, возвращает пустой список"""
    result: List[Any] = open_json_file('missing_file.json')
    assert result == []
    # Проверяем, что os.path.exists был вызван с правильным аргументом
    mock_exists.assert_called_once_with('missing_file.json')


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_open_json_empty(mock_file: Mock, mock_exists: Mock) -> None:
    """Тест: пустой файл, возвращает пустой список"""
    # Настраиваем моки
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = ''

    result: List[Any] = open_json_file('test.json')

    # Проверяем вызовы
    mock_exists.assert_called_once_with('test.json')
    mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    assert result == []


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_open_json_not_list(mock_file: Mock, mock_exists: Mock) -> None:
    """Тест: JSON содержит объект, а не список → пустой список"""
    test_data: Dict[str, Any] = {'key': 'value'}
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = json.dumps(test_data)

    result: List[Any] = open_json_file('test.json')

    mock_exists.assert_called_once_with('test.json')
    assert result == []


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_valid_list_with_mock(mock_file: Mock, mock_exists: Mock) -> None:
    """Тест: валидный JSON‑список → возвращает данные"""
    test_data: List[Dict[str, Any]] = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': 200}
    ]
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = json.dumps(test_data)

    result: List[Any] = open_json_file('test.json')

    mock_exists.assert_called_once_with('test.json')
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[0]['amount'] == 100
    assert result[1]['id'] == 2
    assert result[1]['amount'] == 200


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_json_decode_error_with_mock(mock_file: Mock, mock_exists: Mock) -> None:
    """Тест: ошибка декодирования JSON → пустой список"""
    mock_exists.return_value = True
    mock_file.return_value.read.return_value = '{ "invalid": json }'

    result: List[Any] = open_json_file('test.json')

    mock_exists.assert_called_once_with('test.json')
    assert result == []
