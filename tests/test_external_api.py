from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_to_rubles


@patch('requests.get')
def test_convert_usd_to_rub(mock_get: Mock) -> None:
    """Тестирование конвертации USD в рубли"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'success': True,
        'result': 900.0
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {'amount': 10, 'currency': 'USD'}
    result = convert_to_rubles(transaction)
    assert result == 900.0


@patch('requests.get', side_effect=requests.RequestException("Network error"))
def test_convert_with_api_error(mock_get: Mock) -> None:
    """Тестирование обработки ошибки сетевого запроса"""
    transaction: Dict[str, Any] = {'amount': 10, 'currency': 'USD'}

    with pytest.raises(ConnectionError) as exc_info:
        convert_to_rubles(transaction)

    assert "Ошибка сетевого запроса" in str(exc_info.value)
    mock_get.assert_called_once()


@patch('requests.get')
def test_api_returns_failure(mock_get: Mock) -> None:
    """Тестирование обработки ошибок API"""
    mock_response = Mock()
    mock_response.json.return_value = {'success': False, 'error': {'info': 'Invalid API key'}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {'amount': 10, 'currency': 'USD'}

    with pytest.raises(ValueError) as exc_info:
        convert_to_rubles(transaction)

    assert "Ошибка API: Invalid API key" in str(exc_info.value)


def test_convert_rub_to_rub() -> None:
    """Конвертирование RUB to RUB"""
    transaction: Dict[str, Any] = {'amount': 1000, 'currency': 'RUB'}
    result = convert_to_rubles(transaction)
    assert result == 1000.0


def test_invalid_amount_format() -> None:
    """Тестирование некорректного формата суммы"""
    transaction: Dict[str, Any] = {'amount': 'invalid', 'currency': 'USD'}

    with pytest.raises(ValueError) as exc_info:
        convert_to_rubles(transaction)

    assert "Некорректный формат суммы" in str(exc_info.value)


@patch('requests.get')
def test_missing_result_field(mock_get: Mock) -> None:
    """Тестирование ответа API без результата"""
    mock_response = Mock()
    mock_response.json.return_value = {'success': True}  # Нет поля 'result'
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {'amount': 10, 'currency': 'USD'}

    with pytest.raises(ValueError) as exc_info:
        convert_to_rubles(transaction)
    assert "Поле 'result' отсутствует" in str(exc_info.value)
