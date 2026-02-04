from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> List[Dict[str, str | int]]:
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-03T10:00:00'},
        {'id': 2, 'state': 'PENDING', 'date': '2023-01-01T09:00:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-02T11:00:00'},
    ]


def test_filter_by_state_default(sample_data: List[Dict[str, str | int]]) -> None:
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_pending(sample_data: List[Dict[str, str | int]]) -> None:
    result = filter_by_state(sample_data, 'PENDING')
    assert len(result) == 1
    assert result[0]['state'] == 'PENDING'


def test_sort_by_date_desc(sample_data: List[Dict[str, str | int]]) -> None:
    result = sort_by_date(sample_data)
    dates = [item['date'] for item in result]
    assert dates == [
        '2023-01-03T10:00:00',
        '2023-01-02T11:00:00',
        '2023-01-01T09:00:00'
    ]


def test_sort_by_date_asc(sample_data: List[Dict[str, str | int]]) -> None:
    result = sort_by_date(sample_data, reverse=False)
    dates = [item['date'] for item in result]
    assert dates == [
        '2023-01-01T09:00:00',
        '2023-01-02T11:00:00',
        '2023-01-03T10:00:00'
    ]


def test_sort_by_date_missing_key() -> None:
    data = [{'id': 1}]
    with pytest.raises(KeyError):
        sort_by_date(data)
