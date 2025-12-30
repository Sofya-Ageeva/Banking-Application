from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card

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

    new_state = filter_by_state(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(new_state)

    sorted_list = sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(sorted_list)
