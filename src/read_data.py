import pandas as pd
from typing import List, Dict, Any

def read_transaction_from_csv(file_path: str) ->List[Dict[str, Any]]:
    """Чтение данных о транзакциях из файла формата .csv"""
    try:
        df = pd.read_csv(file_path)
        if df.empy:
            raise pd.errors.EmptyDataError('Отсутствуют данные для чтения')
        return df.to_dict('records')
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except pd.errors.EmptyDataError as f:
        raise pd.errors.EmptyDataError(f"Ошибка чтения файла: {f}")
    except Exception as f:
        raise Exception(f"Ошибка при чтении файла: {f}")


def read_transaction_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Чтение данных о транзакциях из файла формата .xlsx"""
    try:
        df = pd.read_excel(file_path)
        if df.empy:
            raise  ValueError("Отсутствуют данные для чтения")
        return df.to_dict('records')
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except ValueError as f:
        raise ValueError(f"Ошибка чтения файла: {f}")
    except Exception as f:
        raise Exception(f"Ошибка при чтении файла: {f}")



