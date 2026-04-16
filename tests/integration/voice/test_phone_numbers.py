import pytest
from libzapi import Voice


def test_list_phone_numbers(voice: Voice):
    numbers = list(voice.phone_numbers.list_all())
    assert isinstance(numbers, list)


def test_list_and_get_phone_number(voice: Voice):
    numbers = list(voice.phone_numbers.list_all())
    if not numbers:
        pytest.skip("No phone numbers found")
    number = voice.phone_numbers.get(numbers[0].id)
    assert number.id == numbers[0].id


def test_search_available_numbers(voice: Voice):
    results = voice.phone_numbers.search(country="US")
    assert isinstance(results, list)
