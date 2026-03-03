import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize("masked_data, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("Счёт 73654108430135874305", "Счёт **4305"),
    ("Счет 64686473678894779589", "Счет **9589"),
    ("Счет 35383033474447895560", "Счет **5560"),
])
def test_mask_account_card_valid(masked_data: str, expected: str) -> None:
    """Проверяет корректную маскировку для разных типов карт и счетов."""
    result = mask_account_card(masked_data)
    assert result == expected


@pytest.mark.parametrize("invalid_input", [
    "",
    "   ",
    "VisaPlatinum1234",
    "123456789012",
    "Card 1234ABCD5678",
    "Счет ABC123",
])
def test_mask_account_card_invalid_format(invalid_input: str) -> None:
    """Проверяет, что функция поднимает ValueError на некорректных входных данных."""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


def test_mask_account_card_whitespace_and_case() -> None:
    """Проверяет устойчивость к лишним пробелам и разному регистру."""
    masked_data = "  Visa   Gold    5999414228426353  "
    result = mask_account_card(masked_data)
    assert result == "Visa Gold 5999 41** **** 6353"


def test_mask_account_card_edge_cases() -> None:
    """Проверяет граничные случаи длины номера."""
    with pytest.raises(ValueError):
        mask_account_card("Visa 1234")
    long_account = "Счет " + "1" * 30
    result = mask_account_card(long_account)
    assert result.startswith("Счет **") and len(result) > 6


@pytest.mark.parametrize("input_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-25T10:30:00", "25.12.2023"),
    ("2020-01-01T00:00:00", "01.01.2020"),
    ("2024-03-11T02:26:18Z", "11.03.2024"),
    ("2024-03-11T02:26:18+00:00", "11.03.2024"),
    ("2024-03-11", "11.03.2024"),
])
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Проверяет корректное преобразование разных форматов ISO."""
    result = get_date(input_date)
    assert result == expected


@pytest.mark.parametrize("invalid_date", [
    "",                  # пустая строка
    "   ",               # пробелы
    "11/03/2024",        # неверный разделитель
    "03-11-2024",        # неверный порядок
    "2024/03/11",        # неверные разделители
    "not-a-date",        # не дата
    "2024-13-01T00:00",  # неверный месяц
    "2024-00-10T00:00",  # неверный месяц
    "2024-02-30T00:00",  # неверная дата (февраля 30)
])
def test_get_date_invalid(invalid_date: str) -> None:
    """Проверяет, что функция поднимает ValueError на некорректных датах."""
    with pytest.raises(ValueError):
        get_date(invalid_date)


def test_get_date_none() -> None:
    """Проверяет обработку None."""
    with pytest.raises(ValueError):
        get_date(None)  # type: ignore


def test_get_date_non_string() -> None:
    """Проверяет обработку нестроковых входных данных."""
    with pytest.raises(ValueError):
        get_date(12345)  # type: ignore
    with pytest.raises(ValueError):
        get_date([])  # type: ignore


def test_get_date_edge_dates() -> None:
    """Проверяет крайние допустимые даты."""
    assert get_date("1900-01-01") == "01.01.1900"
    assert get_date("9999-12-31") == "31.12.9999"


def test_get_date_milliseconds() -> None:
    """Проверяет обработку миллисекунд и дробных секунд."""
    result = get_date("2024-03-11T02:26:18.123")
    assert result == "11.03.2024"


def test_get_date_timezone_offset() -> None:
    """Проверяет даты с часовыми поясами."""
    result = get_date("2024-03-11T05:26:18+03:00")
    assert result == "11.03.2024"
