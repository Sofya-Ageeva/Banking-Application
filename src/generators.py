from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]],
                       currency_code: str) -> Generator[Dict[str, Any], None, None]:
    """Функция фильтрации транзакций по коду валюты"""
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount")
        if operation_amount is None:
            continue
        currency_get = operation_amount.get("currency")
        if currency_get is None:
            continue
        currency = currency_get.get("code")
        if currency == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генератор, возвращающий описание транзакций"""
    for transaction in transactions:
        description = transaction.get("description", "")
        yield (lambda x: x if x is not None else "")(description)


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор номеров банковских карт"""
    for number in range(start, stop + 1):
        generate_num = ("0" * 16 + str(number))[-16:]
        formatted_num = f"{generate_num[:4]} {generate_num[4:8]} {generate_num[8:12]} {generate_num[12:]}"
        yield formatted_num
