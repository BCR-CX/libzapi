import pytest

from libzapi import CustomData


def test_list_objects_and_get(custom_data: CustomData):
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    items = list(custom_data.custom_object_fields.list_all(objects[0].key))
    assert len(items) > 0, "Expected at least 1 custom object fields"
