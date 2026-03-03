from typing import List

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def valid_card_numbers() -> List[str]:
    """Валидные номера карт в разных форматах."""
    return [
        "1234567890123456",
        "1234 5678 9012 3456",
        "1234-5678-9012-3456",
        "  1234  5678  9012  3456  ",
        "1234-5678 9012-3456",
    ]


@pytest.fixture
def invalid_card_numbers() -> List[str]:
    """Невалидные номера карт (длина ≠ 16 или не цифры)."""
    return [
        "",
        "123",
        "abcd1234",
        "11111111111111111",  # 17 символов
        "12-34",
        "1234a5678b9012c3456",
        "    ",
    ]


@pytest.fixture
def valid_account_numbers() -> List[str]:
    """Валидные номера счетов (≥ 20 символов)."""
    return [
        "73654108430135874305",
        "00001234567890123456789",
        "1" * 20,
        "abcdefghijklmnopqrstuvwxyz",
    ]


@pytest.fixture
def short_account_numbers() -> List[str]:
    """Короткие номера счетов (< 20 символов)."""
    return [
        "",
        "123",
        "abc",
        "1234567890123456789",  # 19 символов
        " ",
        "a",
    ]


def test_get_mask_card_number_valid(valid_card_numbers: List[str]) -> None:
    """Проверка маскировки валидных номеров карт."""
    for card in valid_card_numbers:
        result = get_mask_card_number(card)
        # Должно быть 19 символов: 4 блока × 4 + 3 пробела
        assert len(result) == 19
        # Блоки разделены пробелами
        parts = result.split()
        assert len(parts) == 4
        # Первый блок: первые 4 цифры исходного номера
        assert parts[0] == card.replace(" ", "").replace("-", "")[:4]
        # Второй блок: первые 2 цифры + **
        cleaned = card.replace(" ", "").replace("-", "")
        assert parts[1] == cleaned[4:6] + "**"
        # Третий блок: ****
        assert parts[2] == "****"
        # Четвёртый блок: последние 4 цифры
        assert parts[3] == cleaned[-4:]


def test_get_mask_card_number_invalid(invalid_card_numbers: List[str]) -> None:
    """Невалидные номера возвращаются без изменений."""
    for card in invalid_card_numbers:
        assert get_mask_card_number(card) == card


def test_get_mask_card_number_edge_cases() -> None:
    """Граничные случаи: пустые строки, пробелы."""
    assert get_mask_card_number("") == ""
    assert get_mask_card_number("    ") == "    "
    assert get_mask_card_number(" 1 2 3 ") == " 1 2 3 "


def test_get_mask_card_number_mixed_format() -> None:
    """Смешанные разделители (пробелы + дефисы)."""
    input_str = "1234-5678 9012-3456"
    result = get_mask_card_number(input_str)
    expected = "1234 56** **** 3456"
    assert result == expected


def test_get_mask_account_valid(valid_account_numbers: List[str]) -> None:
    """Маскировка валидных номеров счетов."""
    for acc in valid_account_numbers:
        result = get_mask_account(acc)
        expected = "**" + acc.strip()[-4:]
        assert result == expected
        assert len(result) == 6  # "**XXXX


def test_get_mask_account_short_raises_error(short_account_numbers: List[str]) -> None:
    """Короткие номера счетов поднимают ValueError."""
    for acc in short_account_numbers:
        with pytest.raises(ValueError) as excinfo:
            get_mask_account(acc)
        assert "Номер счёта должен содержать не менее 20 символов" in str(excinfo.value)


def test_get_mask_account_whitespace() -> None:
    """Учёт пробелов в начале/конце (strip)."""
    input_str = "   73654108430135874305   "
    result = get_mask_account(input_str)
    assert result == "**4305"


def test_get_mask_account_min_length() -> None:
    """Ровно 20 символов — валидно."""
    acc = "a" * 20
    result = get_mask_account(acc)
    assert result == "**" + "a" * 4


def test_get_mask_account_long_string() -> None:
    """Длинная строка (> 20) — маскируются последние 4."""
    acc = "x" * 25
    result = get_mask_account(acc)
    assert result == "**" + "x" * 4
