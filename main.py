from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date


if __name__ == "__main__":
    masked_card = get_mask_card_number("1234567890123456")
    print(masked_card)
    masked_account = get_mask_account("73654108430135874305")
    print(masked_account)
    masked_data = mask_account_card("Visa Platinum 7000792289606361")
    print(masked_data)
    masked_data = mask_account_card("Счет 73654108430135874305")
    print(masked_data)
    formated_date = get_date("2024-03-11T02:26:18.671407")
    print(formated_date)