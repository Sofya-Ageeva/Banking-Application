def filter_by_state(filterable_state: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и
    возвращает новый словарь со значением по умолчанию"""

    result = []
    for states in filterable_state:
        if states.get('state') == state:
            result.append(states)
    return result


