import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_field(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        key=f"libzapi_{suffix}",
        type="text",
        title=f"libzapi field {suffix}",
    )
    defaults.update(overrides)
    return ticketing.user_fields.create(**defaults)


def test_list_and_get_user_fields(ticketing: Ticketing):
    objs = list(itertools.islice(ticketing.user_fields.list_all(), 20))
    assert len(objs) > 0
    obj = ticketing.user_fields.get_by_id(objs[0].id)
    assert obj.key == objs[0].key


def test_create_update_delete_field(ticketing: Ticketing):
    field = _create_field(ticketing, description="created by libzapi")
    assert field.id > 0
    try:
        updated = ticketing.user_fields.update(
            field.id, description="updated by libzapi", active=False
        )
        assert updated.description == "updated by libzapi"
        assert updated.active is False
    finally:
        ticketing.user_fields.delete(field.id)


def test_dropdown_options_lifecycle(ticketing: Ticketing):
    field = _create_field(
        ticketing,
        type="dropdown",
        custom_field_options=[
            {"name": "Alpha", "value": f"alpha_{_unique()}"},
        ],
    )
    try:
        options = list(ticketing.user_fields.list_options(field.id))
        assert len(options) >= 1

        created = ticketing.user_fields.upsert_option(
            user_field_id=field.id,
            name="Beta",
            value=f"beta_{_unique()}",
        )
        assert created.id

        fetched = ticketing.user_fields.get_option_by_id(
            user_field_id=field.id, user_field_option_id=created.id
        )
        assert fetched.id == created.id

        ticketing.user_fields.delete_option(
            user_field_id=field.id, user_field_option_id=created.id
        )
    finally:
        ticketing.user_fields.delete(field.id)


def test_reorder_does_not_raise(ticketing: Ticketing):
    fields = list(itertools.islice(ticketing.user_fields.list_all(), 5))
    ids = [f.id for f in fields]
    ticketing.user_fields.reorder(ids)
