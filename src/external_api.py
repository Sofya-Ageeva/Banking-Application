import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def conversion_to_rubles(transaction: Dict[str, Any]) -> float:
    """Принимает на вход транзакцию и конвертирует валюту EUR/USD в рубли"""
    url = "https://api.apilayer.com/exchangerates_data/convert"
    operation_amount = transaction.get('operationAmount', {})
    amount_str = operation_amount.get('amount', '0')
    currency_data = operation_amount.get('currency', {})
    from_currency = currency_data.get('code', 'RUB').upper()

    # Преобразуем строку в число
    try:
        amount = float(amount_str)
    except ValueError:
        raise ValueError(f"Некорректный формат суммы: {amount_str}")

    if from_currency == 'RUB':
        return amount

    # Получаем API‑ключ из переменных окружения
    api_key = os.getenv('APILAYER_API_KEY')
    if not api_key:
        raise ValueError("Ключ не найден в переменных окружения")

    params = {
        'to': 'RUB',
        'from': from_currency,
        'amount': amount
    }
    headers = {
        'apikey': api_key
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        # Проверяем успешность операции
        if not data.get('success', False):
            error_msg = data.get('error', {}).get('info', 'Неизвестная ошибка API')
            raise ValueError(f"Ошибка API: {error_msg}")

        # Извлекаем результат конвертации
        converted_amount = data.get('result')
        if converted_amount is None:
            raise ValueError("Поле 'result' отсутствует в ответе API")

        return round(converted_amount, 2)

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе курса валют: {e}")
    except KeyError as e:
        raise ValueError(f"Некорректный ответ API: отсутствует поле {e}")
