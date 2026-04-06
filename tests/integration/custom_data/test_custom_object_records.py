import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key(custom_data: CustomData) -> str:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    return objects[0].key


def test_list_objects_and_get(custom_data: CustomData, custom_object_key: str):
    items = list(custom_data.custom_object_records.list_all(custom_object_key))
    assert len(items) > 0, "Expected at least 1 custom object records"


def test_list_objects_and_get_with_sort_and_pagination(custom_data: CustomData, custom_object_key: str):
    items = list(
        custom_data.custom_object_records.list_all(
            custom_object_key=custom_object_key, sort_type="id", sort_order="asc", page_size=2
        )
    )
    assert len(items) > 0, "Expected at least 1 custom object records"


def test_list_records_limit(custom_data: CustomData):
    limit = custom_data.custom_object_records.limit()
    assert limit.limit > 0, "Expected record limit to be greater than 0"


def test_count_records(custom_data: CustomData, custom_object_key: str):
    count = custom_data.custom_object_records.count(custom_object_key)
    assert count.value >= 0


def test_search_records(custom_data: CustomData, custom_object_key: str):
    results = list(custom_data.custom_object_records.search(custom_object_key, query="*"))
    assert isinstance(results, list)


def test_autocomplete_records(custom_data: CustomData, custom_object_key: str):
    results = list(custom_data.custom_object_records.autocomplete(custom_object_key, name="a"))
    assert isinstance(results, list)


def test_create_update_delete_record(custom_data: CustomData, custom_object_key: str):
    record = custom_data.custom_object_records.create(
        custom_object_key=custom_object_key,
        name="Integration Test Record",
    )
    assert record.id is not None

    try:
        fetched = custom_data.custom_object_records.get(custom_object_key, record.id)
        assert fetched.id == record.id
    finally:
        custom_data.custom_object_records.delete(custom_object_key, record.id)
