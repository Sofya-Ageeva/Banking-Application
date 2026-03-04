import logging

logger = logging.getLogger('masks')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/masks.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция шифрования номера карты пользователя"""
    try:
        # Очищаем номер от пробелов и дефисов
        cleaned = card_number.replace(" ", "").replace("-", "")
        if len(cleaned) != 16 or not cleaned.isdigit():
            raise ValueError("Некорректный номер карты")
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
    except ValueError as e:
        logger.error(f'Произошла ошибка функции get_mask_card_number: {e}')
    except Exception as e:
        logger.error(f'Произошла ошибка функции get_mask_card_number: {e}')
    return card_number


masked_card = get_mask_card_number("1234567890123456")
print(masked_card)


def get_mask_account(account_number: str) -> str:
    """Функция шифрования счета пользователя"""
    cleaned = account_number.strip()
    if len(cleaned) < 20:
        error_msg = "Номер счёта должен содержать не менее 20 символов"
        logger.error('Произошла ошибка в функции get_mask_account')
        raise ValueError(error_msg)
    return "**" + cleaned[-4:]


masked_account = get_mask_account("73654108430135874300")
print(masked_account)
