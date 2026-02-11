from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """Функция фильтрации транзакций по коду валюты"""

    for transaction in transactions:
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if currency == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, возвращающий описание транзакций"""
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


def card_number_generator(start: int, stop: int) -> str:
    for number in range(start, stop + 1):
        generate_num = ("0" * 16 + str(number))[-16:]
        formatted_num = f"{generate_num[:4]} {generate_num[4:8]} {generate_num[8:12]} {generate_num[12:]}"
        yield formatted_num
