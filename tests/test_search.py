import pytest
from src.search import process_bank_search, process_bank_operations


TEST_DATA = [
    {'id': 1, 'description': 'Перевод с карты на карту', 'amount': '130 USD'},
    {'id': 2, 'description': 'Открытие вклада', 'amount': '40542 руб.'},
    {'id': 3, 'description': 'Оплата в магазине', 'amount': '500 руб.'}
]


def test_process_bank_search_found():
    """Тест поиска по описанию — совпадение найдено."""
    result = process_bank_search(TEST_DATA, 'Перевод')
    assert len(result) == 1
    assert result[0]['id'] == 1


def test_process_bank_search_not_found():
    """Тест поиска по описанию — совпадения нет."""
    result = process_bank_search(TEST_DATA, 'Покупка')
    assert len(result) == 0


def test_process_bank_operations_count():
    """Тест подсчёта операций по категориям."""
    categories = ['Перевод', 'Открытие']
    result = process_bank_operations(TEST_DATA, categories)
    assert 'Перевод' in result
    assert 'Открытие' in result
    assert result['Перевод'] == 1
    assert result['Открытие'] == 1
