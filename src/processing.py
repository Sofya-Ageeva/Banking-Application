from typing import List, Dict, Any


def filter_by_state(filterable_state: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Функция принимает список словарей и
    возвращает новый словарь со значением по умолчанию"""

    result = []
    for states in filterable_state:
        if states.get("state") == state:
            result.append(states)
    return result


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате"""
    for item in data:
        if "date" not in item:
            raise KeyError("Отсутствует ключ 'date'")
    return sorted(data, key=lambda x: x["date"], reverse=reverse)
