from libzapi.application.commands.ticketing.ticket_trigger_cmds import (
    CreateTicketTriggerCmd,
    UpdateTicketTriggerCmd,
)
from libzapi.infrastructure.mappers.ticketing.ticket_trigger_mapper import (
    to_payload_create,
    to_payload_update,
)


_ACTIONS = [{"field": "status", "value": "open"}]
_CONDS = {"all": [{"field": "update_type", "operator": "is", "value": "Create"}], "any": []}


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateTicketTriggerCmd(title="T", actions=_ACTIONS)
    )
    assert payload == {"trigger": {"title": "T", "actions": _ACTIONS}}


def test_create_includes_all_optional_fields():
    cmd = CreateTicketTriggerCmd(
        title="T",
        actions=_ACTIONS,
        conditions=_CONDS,
        active=True,
        description="d",
        category_id="123",
        position=2,
    )
    body = to_payload_create(cmd)["trigger"]
    assert body["title"] == "T"
    assert body["actions"] == _ACTIONS
    assert body["conditions"] == _CONDS
    assert body["active"] is True
    assert body["description"] == "d"
    assert body["category_id"] == "123"
    assert body["position"] == 2


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateTicketTriggerCmd(title="T", actions=_ACTIONS, active=False)
    )["trigger"]
    assert body["active"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateTicketTriggerCmd(title="T", actions=_ACTIONS)
    )["trigger"]
    assert "active" not in body
    assert "conditions" not in body
    assert "description" not in body
    assert "category_id" not in body
    assert "position" not in body


def test_create_converts_actions_iterable_to_list():
    body = to_payload_create(
        CreateTicketTriggerCmd(title="T", actions=iter(_ACTIONS))
    )["trigger"]
    assert body["actions"] == _ACTIONS


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateTicketTriggerCmd()) == {"trigger": {}}


def test_update_includes_all_fields():
    cmd = UpdateTicketTriggerCmd(
        title="New",
        actions=_ACTIONS,
        conditions=_CONDS,
        active=True,
        description="d",
        category_id="42",
        position=7,
    )
    body = to_payload_update(cmd)["trigger"]
    assert body == {
        "title": "New",
        "actions": _ACTIONS,
        "conditions": _CONDS,
        "active": True,
        "description": "d",
        "category_id": "42",
        "position": 7,
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateTicketTriggerCmd(active=False))["trigger"]
    assert body == {"active": False}


def test_update_converts_actions_iterable_to_list():
    body = to_payload_update(
        UpdateTicketTriggerCmd(actions=iter(_ACTIONS))
    )["trigger"]
    assert body["actions"] == _ACTIONS
