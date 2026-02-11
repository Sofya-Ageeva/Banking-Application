import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator



@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Покупка в магазине",
            "from": "Visa 1234",
            "to": "MasterCard 5678"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T11:00:00",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "EUR", "code": "EUR"}
            },
            "description": "Онлайн-оплата",
            "from": "MasterCard 9012",
            "to": "Visa 3456"
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2023-01-03T12:00:00",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Возврат средств",
            "from": "Sber 7777",
            "to": "Tinkoff 8888"
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций."""
    return []


# --- Тесты для filter_by_currency ---

@pytest.mark.parametrize(
    "currency_code, expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("RUB", []),  # валюты нет
    ]
)
def test_filter_by_currency(sample_transactions, currency_code, expected_ids):
    """Проверяем фильтрацию по валюте."""
    filtered = list(filter_by_currency(sample_transactions, currency_code))
    assert len(filtered) == len(expected_ids)
    assert [t["id"] for t in filtered] == expected_ids


def test_filter_by_currency_empty_list(empty_transactions):
    """Фильтр на пустом списке — должен вернуть пустой итератор."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []


def test_filter_by_currency_no_currency_field(sample_transactions):
    """Транзакция без поля operationAmount.currency — не должна вызвать ошибку."""
    # Модифицируем одну транзакцию: убираем currency
    sample_transactions[0]["operationAmount"]["currency"] = None

    filtered = list(filter_by_currency(sample_transactions, "USD"))
    # Только транзакция с id=3 имеет валидный USD
    assert len(filtered) == 1
    assert filtered[0]["id"] == 3


# --- Тесты для transaction_descriptions ---

def test_transaction_descriptions(sample_transactions):
    """Проверяем возврат описаний."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Покупка в магазине",
        "Онлайн-оплата",
        "Возврат средств"
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list(empty_transactions):
    """На пустом списке должен вернуться пустой итератор."""
    result = list(transaction_descriptions(empty_transactions))
    assert result == []


def test_transaction_descriptions_missing_description(sample_transactions):
    """Если description отсутствует — возвращаем пустую строку."""
    sample_transactions[1]["description"] = None  # убираем описание

    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions[1] == ""  # None → ""


# --- Тесты для card_number_generator ---

@pytest.mark.parametrize(
    "start, end, expected_first, expected_last",
    [
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (9999999999999998, 9999999999999999, "9999 9999 9999 9998", "9999 9999 9999 9999"),
        (1000000000000000, 1000000000000000, "1000 0000 0000 0000", "1000 0000 0000 0000"),
    ]
)

def test_card_number_generator_range(start, end, expected_first, expected_last):
    """Проверяем генерацию в разных диапазонах."""
    cards = list(card_number_generator(start, end))
    assert cards[0] == expected_first
    assert cards[-1] == expected_last
    assert len(cards) == (end - start + 1)


def test_card_number_generator_single():
    """Генератор одного номера."""
    cards = list(card_number_generator(42, 42))
    assert cards == ["0000 0000 0000 0042"]


def test_card_number_generator_formatting():
    """Проверяем формат: 4 группы по 4 цифры через пробел."""
    cards = list(card_number_generator(1234567890123456, 1234567890123456))
    assert cards[0] == "1234 5678 9012 3456"



def test_card_number_generator_invalid_range():
    """При start > end генератор должен вернуть пустой итератор."""
    cards = list(card_number_generator(10, 5))
    assert cards == []


def test_card_number_generator_edge_cases():
    """Крайние значения: min и max."""
    min_card = list(card_number_generator(1, 1))
    max_card = list(card_number_generator(9999999999999999, 9999999999999999))

    assert min_card[0] == "0000 0000 0000 0001"
    assert max_card[0] == "9999 9999 9999 9999"
