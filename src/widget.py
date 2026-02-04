from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(masked_data: str) -> str:
    """Маскирует номер карты или номер счета"""
    name_type = ' '.join(masked_data.strip().split())
    if not name_type:
        raise ValueError("Отсутствуют введенные данные")

    if not isinstance(masked_data, str):
        raise ValueError("Неверный тип данных")
    parts = name_type.rsplit(" ", 1)

    if len(parts) != 2:
        raise ValueError("Некорректный формат: введите тип и номер карты")

    parts_type, number = parts
    if not number.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    if parts_type in ("Счёт", "Счет"):
        if len(number) < 4:
            raise ValueError("Номер счёта слишком короткий")
        mask_account_number = get_mask_account(number)
    else:
        if len(number) not in (16, 18, 19):
            raise ValueError("Некорректная длина номера карты")
        mask_account_number = get_mask_card_number(number)
    return f"{parts_type} {mask_account_number}"


def get_date(formated_date: str) -> str:
    """Функция форматирования даты"""
    if not isinstance(formated_date, str):
        raise ValueError("Входные данные должны быть строкой")

    cleaned = formated_date.strip()
    if not cleaned:
        raise ValueError("Пустая строка")

    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    elif "T" not in cleaned and "+" not in cleaned and "-" not in cleaned[1:]:
        cleaned += "+00:00"

    try:
        date = datetime.fromisoformat(cleaned)

        if not (1 <= date.year <= 9999):
            raise ValueError("Год должен быть от 1 до 9999")
        return date.strftime("%d.%m.%Y")

    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидаемый формат: ГГГГ-ММ-ДД")
