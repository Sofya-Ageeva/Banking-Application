from typing import List, Dict, Any


def filter_by_state(filterable_state: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Функция принимает список словарей и
    возвращает новый словарь со значением по умолчанию"""

    result = []
    for states in filterable_state:
        if states.get("state") == state:
            result.append(states)
    return result


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате"""
    return sorted(data, key=lambda x: x["date"], reverse=reverse)
