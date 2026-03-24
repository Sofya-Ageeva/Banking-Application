import os
from typing import Any, Dict, List, cast

from src.read_data import read_transaction_from_csv, read_transaction_from_excel
from src.search import process_bank_search
from src.utils import open_json_file
from src.widget import get_date, mask_account_card

AVAILABLE_STATUS = {'EXECUTED', 'CANCELED', 'PENDING'}


def main() -> None:
    """Основной функционал программы с пользовательским интерфейсом."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    mode_selection = input().strip()

    # Загрузка данных в зависимости от выбора
    try:
        if mode_selection == '1':
            file_path = input("Введите путь к JSON-файлу: ").strip()
            if not os.path.exists(file_path):
                print("Не удалось загрузить транзакции. Проверьте путь к файлу и его содержимое.")
                return
            transactions = open_json_file(file_path)
        elif mode_selection == '2':
            file_path = input("Введите путь к CSV-файлу: ").strip()
            if not os.path.exists(file_path):
                print("Не удалось загрузить транзакции. Проверьте путь к файлу и его содержимое.")
                return
            transactions = cast(List[Dict[str, Any]], read_transaction_from_csv(file_path))
        elif mode_selection == '3':
            file_path = input("Введите путь к XLSX-файлу: ").strip()
            if not os.path.exists(file_path):
                print("Не удалось загрузить транзакции. Проверьте путь к файлу и его содержимое.")
                return
            transactions = cast(List[Dict[str, Any]], read_transaction_from_excel(file_path))
        else:
            print("Неверный выбор. Завершение программы.")
            return
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    print(f"Для обработки выбран {['JSON', 'CSV', 'XLSX'][int(mode_selection) - 1]}-файл.")

    # Фильтрация по статусу
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()

        if status in AVAILABLE_STATUS:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            filtered_transactions = [
                t for t in transactions if t.get('state', '').upper() == status
            ]
            print(f"Найдено транзакций с состоянием {status}: {len(filtered_transactions)}")
            break
        else:
            print(f"Статус операции \"{status}\" недоступен. Попробуйте ещё раз:")

    # Сортировка по дате
    sort_by_date = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_by_date in ['да', 'yes', 'y']:
        while True:
            order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
            if order in ['по возрастанию', 'по возрастанию']:
                reverse = False
                break
            elif order == 'по убыванию':
                reverse = True
                break
            else:
                print("Некорректный порядок сортировки. Введите 'по возрастанию' или 'по убыванию'.")
        if filtered_transactions and 'date' in filtered_transactions[0]:
            filtered_transactions.sort(
                key=lambda x: x.get('date', ''),
                reverse=reverse
            )

    # Фильтрация по валюте (рублёвые)
    rub_only = input("Выводить только рублёвые транзакции? Да/Нет\n").strip().lower()
    if rub_only in ['да', 'yes', 'y']:
        filtered_transactions = [
            t for t in filtered_transactions
            if 'руб' in t.get('operationAmount', {}).get('currency', {}).get('name', '').lower()
        ]

    # Поиск по описанию
    search_needed = input("Отфильтровать список транзакций по определённому слову в описании? "
                          "Да/Нет\n").strip().lower()
    if search_needed in ['да', 'yes', 'y']:
        search_query = input("Введите строку для поиска в описании:\n").strip()
        filtered_transactions = process_bank_search(filtered_transactions, search_query)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for i, transaction in enumerate(filtered_transactions, start=1):
            date = get_date(transaction.get('date', 'N/A'))
            desc = transaction.get('description', 'N/A')

            # Получаем номер счёта/карты из поля 'from' или 'to' и маскируем
            from_account = transaction.get('from', '')
            to_account = transaction.get('to', '')
            # Формируем строку перевода: обрабатываем случаи с from и to отдельно
            transfer_info = 'N/A'
            if from_account and to_account:
                # Маскируем оба номера по отдельности
                try:
                    from_masked = mask_account_card(from_account)
                except ValueError:
                    from_masked = from_account
                try:
                    to_masked = mask_account_card(to_account)
                except ValueError:
                    to_masked = to_account
                transfer_info = f"{from_masked} -> {to_masked}"
            elif from_account:
                try:
                    transfer_info = mask_account_card(from_account)
                except ValueError:
                    transfer_info = from_account
            elif to_account:
                try:
                    transfer_info = mask_account_card(to_account)
                except ValueError:
                    transfer_info = to_account

            amount_info = transaction.get('operationAmount', {})
            amount = amount_info.get('amount', 'N/A')
            currency_info = amount_info.get('currency', {})
            currency = currency_info.get('name', 'N/A')

            print(f"\n{i}. {date} {desc}")
            print(transfer_info)
            print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
