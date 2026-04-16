import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key(custom_data: CustomData) -> str:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    return objects[0].key


def test_list_access_rules(custom_data: CustomData, custom_object_key: str):
    rules = list(custom_data.access_rules.list_all(custom_object_key))
    assert isinstance(rules, list)


def test_definitions(custom_data: CustomData, custom_object_key: str):
    defs = custom_data.access_rules.definitions(custom_object_key)
    assert isinstance(defs, dict)
