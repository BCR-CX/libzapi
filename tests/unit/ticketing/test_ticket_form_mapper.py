from libzapi.application.commands.ticketing.ticket_form_cmds import (
    CreateTicketFormCmd,
    UpdateTicketFormCmd,
)
from libzapi.infrastructure.mappers.ticketing.ticket_form_mapper import (
    to_payload_create,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateTicketFormCmd(name="Default", ticket_field_ids=[1, 2])
    )
    assert payload == {
        "ticket_form": {"name": "Default", "ticket_field_ids": [1, 2]}
    }


def test_create_includes_all_optional_fields():
    cmd = CreateTicketFormCmd(
        name="Default",
        ticket_field_ids=[1, 2],
        display_name="Public",
        end_user_visible=True,
        position=3,
        active=True,
        default=True,
        in_all_brands=True,
        restricted_brand_ids=[10, 20],
        end_user_conditions=[{"parent_field_id": 1, "value": "yes"}],
        agent_conditions=[{"parent_field_id": 2, "value": "no"}],
    )

    body = to_payload_create(cmd)["ticket_form"]

    assert body["name"] == "Default"
    assert body["ticket_field_ids"] == [1, 2]
    assert body["display_name"] == "Public"
    assert body["end_user_visible"] is True
    assert body["position"] == 3
    assert body["active"] is True
    assert body["default"] is True
    assert body["in_all_brands"] is True
    assert body["restricted_brand_ids"] == [10, 20]
    assert body["end_user_conditions"] == [{"parent_field_id": 1, "value": "yes"}]
    assert body["agent_conditions"] == [{"parent_field_id": 2, "value": "no"}]


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateTicketFormCmd(
            name="n",
            ticket_field_ids=[1],
            end_user_visible=False,
            active=False,
            default=False,
            in_all_brands=False,
        )
    )["ticket_form"]
    assert body["end_user_visible"] is False
    assert body["active"] is False
    assert body["default"] is False
    assert body["in_all_brands"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateTicketFormCmd(name="n", ticket_field_ids=[1])
    )["ticket_form"]
    assert set(body.keys()) == {"name", "ticket_field_ids"}


def test_create_converts_iterables_to_lists():
    cmd = CreateTicketFormCmd(
        name="n",
        ticket_field_ids=iter([1, 2]),
        restricted_brand_ids=iter([7]),
        end_user_conditions=iter([{"a": 1}]),
        agent_conditions=iter([{"b": 2}]),
    )
    body = to_payload_create(cmd)["ticket_form"]
    assert body["ticket_field_ids"] == [1, 2]
    assert body["restricted_brand_ids"] == [7]
    assert body["end_user_conditions"] == [{"a": 1}]
    assert body["agent_conditions"] == [{"b": 2}]


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateTicketFormCmd()) == {"ticket_form": {}}


def test_update_includes_all_fields():
    cmd = UpdateTicketFormCmd(
        name="New",
        ticket_field_ids=[3],
        display_name="Public",
        end_user_visible=True,
        position=1,
        active=True,
        default=True,
        in_all_brands=True,
        restricted_brand_ids=[5],
        end_user_conditions=[{"a": 1}],
        agent_conditions=[{"b": 2}],
    )
    body = to_payload_update(cmd)["ticket_form"]
    assert body == {
        "name": "New",
        "ticket_field_ids": [3],
        "display_name": "Public",
        "end_user_visible": True,
        "position": 1,
        "active": True,
        "default": True,
        "in_all_brands": True,
        "restricted_brand_ids": [5],
        "end_user_conditions": [{"a": 1}],
        "agent_conditions": [{"b": 2}],
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateTicketFormCmd(active=False))["ticket_form"]
    assert body == {"active": False}


def test_update_converts_iterables_to_lists():
    body = to_payload_update(
        UpdateTicketFormCmd(
            ticket_field_ids=iter([9]),
            restricted_brand_ids=iter([3]),
            end_user_conditions=iter([{"a": 1}]),
            agent_conditions=iter([{"b": 2}]),
        )
    )["ticket_form"]
    assert body["ticket_field_ids"] == [9]
    assert body["restricted_brand_ids"] == [3]
    assert body["end_user_conditions"] == [{"a": 1}]
    assert body["agent_conditions"] == [{"b": 2}]
