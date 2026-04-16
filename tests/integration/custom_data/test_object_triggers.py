import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key(custom_data: CustomData) -> str:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    return objects[0].key


def test_list_triggers(custom_data: CustomData, custom_object_key: str):
    triggers = list(custom_data.object_triggers.list_all(custom_object_key))
    assert isinstance(triggers, list)


def test_list_active_triggers(custom_data: CustomData, custom_object_key: str):
    triggers = list(custom_data.object_triggers.list_active(custom_object_key))
    assert isinstance(triggers, list)


def test_definitions(custom_data: CustomData, custom_object_key: str):
    defs = custom_data.object_triggers.definitions(custom_object_key)
    assert isinstance(defs, dict)
