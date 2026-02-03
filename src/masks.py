def get_mask_card_number(card_number: str) -> str:
    """Функция шифрования номера карты пользователя"""
    # Очищаем номер от пробелов и дефисов
    cleaned = card_number.replace(" ", "").replace("-", "")
    if len(cleaned) != 16 or not cleaned.isdigit():
        return card_number
    # Зашифровываем символы карты (6-12)
    mask_card_number = cleaned[:6] + "*" * 6 + cleaned[-4:]
    # Разбиваем номер карты на блоки по 4 символа
    block_list = []
    for i in range(0, len(mask_card_number), 4):
        block = mask_card_number[i : i + 4]
        block_list.append(block)
    # Объединяем список в один
    formated_user_card = " ".join(block_list)
    return formated_user_card


def get_mask_account(account_number: str) -> str:
    """Функция шифрования счета пользователя"""
    cleaned = account_number.strip()
    if len(cleaned) < 20:
        raise ValueError("Номер счёта должен содержать не менее 20 символов")
    return "**" + cleaned[-4:]
