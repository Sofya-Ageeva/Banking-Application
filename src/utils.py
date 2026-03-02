import json
import os
from typing import Any, Dict, List


def open_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Функция принимает на вход путь до файла с данными о транзакциях
    и возвращает список словарей"""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            received_data = json.load(f)
            if len(received_data) != 0 and isinstance(received_data, List):
                return received_data
            else:
                return []
    except (json.JSONDecodeError, UnicodeDecodeError, PermissionError):
        return []


test = open_json_file('data/operations.json')
print(test)
