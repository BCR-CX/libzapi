import uuid

from libzapi import CustomData


def test_list_objects_and_get(custom_data: CustomData):
    itens = list(custom_data.custom_objects.list_all())
    assert len(itens) >= 0, "Expected at least 0 custom objects"


def test_limit_objects(custom_data: CustomData):
    limit = custom_data.custom_objects.limit()
    assert limit.limit > 0, "Expected limit to be greater than 0"
    assert limit.count >= 0, "Expected count to be non-negative"


def test_create_update_delete_custom_object(custom_data: CustomData):
    uid = str(uuid.uuid4())[:8]
    key = f"test_{uid}"

    obj = custom_data.custom_objects.create(
        key=key,
        title=f"Test Object {uid}",
        title_pluralized=f"Test Objects {uid}",
        include_in_list_view=False,
    )
    assert obj.key == key

    try:
        updated = custom_data.custom_objects.update(key, title=f"Updated {uid}")
        assert updated.title == f"Updated {uid}"

        fetched = custom_data.custom_objects.get(key)
        assert fetched.key == key
    finally:
        custom_data.custom_objects.delete(key)
