import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key(custom_data: CustomData) -> str:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    return objects[0].key


def test_list_objects_and_get(custom_data: CustomData, custom_object_key: str):
    items = list(custom_data.custom_object_fields.list_all(custom_object_key))
    assert len(items) > 0, "Expected at least 1 custom object fields"


def test_create_and_delete_field(custom_data: CustomData, custom_object_key: str):
    field = custom_data.custom_object_fields.create(
        custom_object_key=custom_object_key,
        type="text",
        key="integration_test_field",
        title="Integration Test Field",
    )
    assert field.key == "integration_test_field"

    try:
        fetched = custom_data.custom_object_fields.get(custom_object_key, field.id)
        assert fetched.id == field.id
    finally:
        custom_data.custom_object_fields.delete(custom_object_key, field.id)
