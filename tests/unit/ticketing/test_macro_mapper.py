from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)
from libzapi.infrastructure.mappers.ticketing.macro_mapper import (
    to_payload_create,
    to_payload_update,
)


_BASIC_ACTIONS = [{"field": "status", "value": "solved"}]


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateMacroCmd(title="Close", actions=_BASIC_ACTIONS)
    )
    assert payload == {
        "macro": {"title": "Close", "actions": _BASIC_ACTIONS}
    }


def test_create_includes_all_optional_fields():
    cmd = CreateMacroCmd(
        title="Close",
        actions=_BASIC_ACTIONS,
        active=True,
        description="hello",
        restriction={"type": "Group", "id": 1},
    )

    body = to_payload_create(cmd)["macro"]

    assert body["title"] == "Close"
    assert body["actions"] == _BASIC_ACTIONS
    assert body["active"] is True
    assert body["description"] == "hello"
    assert body["restriction"] == {"type": "Group", "id": 1}


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateMacroCmd(title="t", actions=_BASIC_ACTIONS, active=False)
    )["macro"]
    assert body["active"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateMacroCmd(title="t", actions=_BASIC_ACTIONS)
    )["macro"]
    assert "active" not in body
    assert "description" not in body
    assert "restriction" not in body


def test_create_converts_actions_iterable_to_list():
    cmd = CreateMacroCmd(title="t", actions=iter(_BASIC_ACTIONS))
    body = to_payload_create(cmd)["macro"]
    assert body["actions"] == _BASIC_ACTIONS


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateMacroCmd()) == {"macro": {}}


def test_update_includes_all_fields():
    cmd = UpdateMacroCmd(
        title="New",
        actions=_BASIC_ACTIONS,
        active=True,
        description="desc",
        restriction={"type": "User", "id": 5},
        position=3,
    )
    body = to_payload_update(cmd)["macro"]
    assert body == {
        "title": "New",
        "actions": _BASIC_ACTIONS,
        "active": True,
        "description": "desc",
        "restriction": {"type": "User", "id": 5},
        "position": 3,
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateMacroCmd(active=False))["macro"]
    assert body == {"active": False}


def test_update_converts_actions_iterable_to_list():
    body = to_payload_update(
        UpdateMacroCmd(actions=iter(_BASIC_ACTIONS))
    )["macro"]
    assert body["actions"] == _BASIC_ACTIONS
