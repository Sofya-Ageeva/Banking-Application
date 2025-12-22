from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(masked_data: str) -> str:
    """Маскирует номер карты или номер счета"""
    name_type = masked_data.strip()
    parts = name_type.rsplit(" ", 1)

    if len(parts) != 2:
        return masked_data

    parts_type, number = parts

    if parts_type == "Счет":
        mask_account_number = get_mask_account(number)
    else:
        mask_account_number = get_mask_card_number(number)

    return f"{parts_type} {mask_account_number}"


def get_date(formated_date: str) -> str:
    """Функция форматирования даты"""
    accepted_date = formated_date.split("T")[0]

    year, month, day = accepted_date.split("-")
    return f"{day}.{month}.{year}"
