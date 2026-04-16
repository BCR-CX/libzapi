import pytest

from libzapi import CustomData


def test_list_record_events(custom_data: CustomData):
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found")
    records = list(custom_data.custom_object_records.list_all(objects[0].key))
    if not records:
        pytest.skip("No records found")
    events = list(custom_data.record_events.list_all(objects[0].key, records[0].id, page_size=10))
    assert isinstance(events, list)
