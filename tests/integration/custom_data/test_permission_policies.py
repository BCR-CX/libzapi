import pytest

from libzapi import CustomData


@pytest.fixture()
def custom_object_key(custom_data: CustomData) -> str:
    objects = list(custom_data.custom_objects.list_all())
    if not objects:
        pytest.skip("No custom objects found in the live API")
    return objects[0].key


def test_list_permission_policies(custom_data: CustomData, custom_object_key: str):
    policies = list(custom_data.permission_policies.list_all(custom_object_key))
    assert isinstance(policies, list)


def test_list_and_get_policy(custom_data: CustomData, custom_object_key: str):
    policies = list(custom_data.permission_policies.list_all(custom_object_key))
    if not policies:
        pytest.skip("No permission policies found")
    policy = custom_data.permission_policies.get(custom_object_key, policies[0].id)
    assert policy.id == policies[0].id
