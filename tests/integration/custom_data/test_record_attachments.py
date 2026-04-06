import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key_and_record(custom_data: CustomData) -> tuple[str, str]:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found")
    # Find an object with allows_attachments enabled
    for obj in objects:
        if obj.allows_attachments:
            records = list(custom_data.custom_object_records.list_all(obj.key))
            if records:
                return obj.key, records[0].id
    pytest.skip("No custom objects with attachments enabled and records found")


def test_list_attachments(custom_data: CustomData, custom_object_key_and_record: tuple[str, str]):
    key, record_id = custom_object_key_and_record
    attachments = list(custom_data.record_attachments.list_all(key, record_id))
    assert isinstance(attachments, list)


def test_download_url(custom_data: CustomData):
    url = custom_data.record_attachments.download_url("obj", "rec", "att")
    assert "/attachments/att/download" in url
