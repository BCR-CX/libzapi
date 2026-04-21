from libzapi.application.commands.ticketing.automation_cmds import (
    CreateAutomationCmd,
    UpdateAutomationCmd,
)
from libzapi.infrastructure.mappers.ticketing.automation_mapper import (
    to_payload_create,
    to_payload_update,
)


_ACTIONS = [{"field": "status", "value": "closed"}]
_CONDS = {"all": [{"field": "SOLVED", "operator": "greater_than", "value": "24"}], "any": []}


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateAutomationCmd(title="A", actions=_ACTIONS, conditions=_CONDS)
    )
    assert payload == {
        "automation": {
            "title": "A",
            "actions": _ACTIONS,
            "conditions": _CONDS,
        }
    }


def test_create_includes_all_optional_fields():
    cmd = CreateAutomationCmd(
        title="A",
        actions=_ACTIONS,
        conditions=_CONDS,
        active=True,
        position=3,
    )
    body = to_payload_create(cmd)["automation"]
    assert body["active"] is True
    assert body["position"] == 3


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateAutomationCmd(
            title="A", actions=_ACTIONS, conditions=_CONDS, active=False
        )
    )["automation"]
    assert body["active"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateAutomationCmd(title="A", actions=_ACTIONS, conditions=_CONDS)
    )["automation"]
    assert "active" not in body
    assert "position" not in body


def test_create_converts_actions_iterable_to_list():
    body = to_payload_create(
        CreateAutomationCmd(
            title="A", actions=iter(_ACTIONS), conditions=_CONDS
        )
    )["automation"]
    assert body["actions"] == _ACTIONS


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateAutomationCmd()) == {"automation": {}}


def test_update_includes_all_fields():
    cmd = UpdateAutomationCmd(
        title="New",
        actions=_ACTIONS,
        conditions=_CONDS,
        active=True,
        position=7,
    )
    body = to_payload_update(cmd)["automation"]
    assert body == {
        "title": "New",
        "actions": _ACTIONS,
        "conditions": _CONDS,
        "active": True,
        "position": 7,
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateAutomationCmd(active=False))["automation"]
    assert body == {"active": False}


def test_update_converts_actions_iterable_to_list():
    body = to_payload_update(
        UpdateAutomationCmd(actions=iter(_ACTIONS))
    )["automation"]
    assert body["actions"] == _ACTIONS
