import os
import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', mode='w')
file_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def open_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Функция принимает на вход путь до файла с данными о транзакциях
    и возвращает список словарей"""
    if not os.path.exists(file_path):
        logger.warning(f"Ошибка: указанный файл отсутствует: {file_path}")
        return []

    try:
        logger.info(f"Открываем файл для чтения: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            received_data = json.load(f)
            if isinstance(received_data, List):
                logger.info("Успешное чтение файла")
                return received_data
            else:
                logger.warning(f"Ошибка чтения: некорректный формат данных в {file_path}")
                return []
    except (json.JSONDecodeError, UnicodeDecodeError, PermissionError,
            FileNotFoundError) as e:
        logger.error(f'Произошла ошибка чтения файла: {e}')
        print(f"Ошибка чтения файла {file_path}: {e}")
        return []


test = open_json_file('data/operations.json')
print(test)
