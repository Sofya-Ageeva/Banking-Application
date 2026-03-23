import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Функция для поиска в списке словарей операций по заданной строке"""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []
    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Функция для подсчета количества банковских операций определенного типа."""
    descriptions = [
        transaction.get('description', '').lower()
        for transaction in data
    ]
    counter = Counter(descriptions)
    result = {}
    for category in categories:
        result[category] = sum(
            count for desc, count in counter.items()
            if category.lower() in desc
        )
    return result
