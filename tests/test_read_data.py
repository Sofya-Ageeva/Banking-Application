from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.read_data import read_transaction_from_csv, read_transaction_from_excel


@patch('pandas.read_csv')
def test_read_transaction_from_csv_success(mock: MagicMock) -> None:
    """Успешное чтение файла .csv"""
    test_data = [
        {'id': 1, 'amount': 1000, 'currency': 'RUB'},
        {'id': 2, 'amount': 2000, 'currency': 'USD'}
    ]
    mock.return_value = pd.DataFrame(test_data)
    result = read_transaction_from_csv('test.csv')

    assert isinstance(result, list)
    assert len(result) == 2
    assert result == test_data
    mock.assert_called_once_with('test.csv')


@patch('pandas.read_csv')
def test_read_transaction_from_csv_empty(mock: MagicMock) -> None:
    """Тестируется вызов исключений при чтении пустого файла"""
    mock.return_value = pd.DataFrame()

    with pytest.raises(pd.errors.EmptyDataError, match="Отсутствуют данные для чтения"):
        read_transaction_from_csv('test.csv')


@patch('pandas.read_csv')
def test_read_transaction_from_csv_file_not(mock: MagicMock) -> None:
    """Тестирование вызова исключения, если файл не найден"""
    mock.side_effect = FileNotFoundError("Файл не найден")

    with pytest.raises(FileNotFoundError, match="Файл не найден: test.csv"):
        read_transaction_from_csv('test.csv')


@patch('pandas.read_excel')
def test_read_transaction_from_excel_success(mock: MagicMock) -> None:
    """Тестирование успешного чтения файла excel"""
    test_data = [
        {'transaction_id': 101, 'sum': 5000, 'type': 'debit'},
        {'transaction_id': 102, 'sum': 3000, 'type': 'credit'}
    ]
    mock.return_value = pd.DataFrame(test_data)
    result = read_transaction_from_excel('test.xlsx')

    assert isinstance(result, list)
    assert len(result) == 2
    assert result == test_data
    mock.assert_called_once_with('test.xlsx')


@patch('pandas.read_excel')
def test_read_transaction_from_excel_empty(mock: MagicMock) -> None:
    """Тестирование вызова исключения при чтении пустого файла"""
    mock.return_value = pd.DataFrame
    with pytest.raises(ValueError, match="Отсутствуют данные для чтения"):
        read_transaction_from_excel('test.xlsx')


@patch('pandas.read_excel')
def test_read_transaction_from_excel_not_file(mock: MagicMock) -> None:
    """Тестирование вызова исключения, если файл не найден"""
    mock.side_effect = FileNotFoundError("Файл не найден")

    with pytest.raises(FileNotFoundError, match="Файл не найден: test.xlsx"):
        read_transaction_from_excel('test.xlsx')
