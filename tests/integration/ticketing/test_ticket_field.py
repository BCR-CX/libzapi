import itertools
import uuid

from libzapi import Ticketing


def _unique() -> str:
    return uuid.uuid4().hex[:10]


def _create_field(ticketing: Ticketing, **overrides):
    suffix = _unique()
    defaults = dict(
        title=f"libzapi field {suffix}",
        type="text",
    )
    defaults.update(overrides)
    return ticketing.ticket_fields.create(**defaults)


def test_list_and_get_ticket_field(ticketing: Ticketing):
    fields = list(itertools.islice(ticketing.ticket_fields.list_all(), 20))
    assert len(fields) > 0
    field = ticketing.ticket_fields.get_by_id(fields[0].id)
    assert field.title == fields[0].title


def test_create_update_delete_field(ticketing: Ticketing):
    field = _create_field(ticketing, description="created by libzapi")
    assert field.id > 0
    try:
        updated = ticketing.ticket_fields.update(
            field.id, description="updated by libzapi", active=False
        )
        assert updated.description == "updated by libzapi"
        assert updated.active is False
    finally:
        ticketing.ticket_fields.delete(field.id)


def test_dropdown_options_lifecycle(ticketing: Ticketing):
    field = _create_field(
        ticketing,
        type="tagger",
        custom_field_options=[
            {"name": "Alpha", "value": f"alpha_{_unique()}"},
        ],
    )
    try:
        options = list(ticketing.ticket_fields.list_options(field.id))
        assert len(options) >= 1

        created = ticketing.ticket_fields.upsert_option(
            field_id=field.id, name="Beta", value=f"beta_{_unique()}"
        )
        assert created["id"]

        fetched = ticketing.ticket_fields.get_option(
            field_id=field.id, option_id=created["id"]
        )
        assert fetched["id"] == created["id"]

        ticketing.ticket_fields.delete_option(
            field_id=field.id, option_id=created["id"]
        )
    finally:
        ticketing.ticket_fields.delete(field.id)


def test_reorder_does_not_raise(ticketing: Ticketing):
    fields = list(itertools.islice(ticketing.ticket_fields.list_all(), 5))
    ids = [f.id for f in fields]
    ticketing.ticket_fields.reorder(ids)
