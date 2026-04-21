from libzapi.application.commands.ticketing.view_cmds import (
    CreateViewCmd,
    UpdateViewCmd,
)
from libzapi.infrastructure.mappers.ticketing.view_mapper import (
    to_payload_create,
    to_payload_update,
)


_ALL = [{"field": "status", "operator": "is", "value": "open"}]
_ANY = [{"field": "priority", "operator": "is", "value": "urgent"}]
_OUTPUT = {"columns": ["subject", "requester"]}


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_title():
    payload = to_payload_create(CreateViewCmd(title="V"))
    assert payload == {"view": {"title": "V"}}


def test_create_includes_all_optional_fields():
    cmd = CreateViewCmd(
        title="V",
        all=_ALL,
        any=_ANY,
        description="d",
        active=True,
        position=3,
        output=_OUTPUT,
        restriction={"type": "Group", "id": 1},
    )
    body = to_payload_create(cmd)["view"]
    assert body["all"] == _ALL
    assert body["any"] == _ANY
    assert body["description"] == "d"
    assert body["active"] is True
    assert body["position"] == 3
    assert body["output"] == _OUTPUT
    assert body["restriction"] == {"type": "Group", "id": 1}


def test_create_preserves_false_booleans():
    body = to_payload_create(CreateViewCmd(title="V", active=False))["view"]
    assert body["active"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(CreateViewCmd(title="V"))["view"]
    assert set(body.keys()) == {"title"}


def test_create_converts_iterables_to_lists():
    body = to_payload_create(
        CreateViewCmd(title="V", all=iter(_ALL), any=iter(_ANY))
    )["view"]
    assert body["all"] == _ALL
    assert body["any"] == _ANY


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateViewCmd()) == {"view": {}}


def test_update_includes_all_fields():
    cmd = UpdateViewCmd(
        title="New",
        all=_ALL,
        any=_ANY,
        description="d",
        active=True,
        position=7,
        output=_OUTPUT,
        restriction={"type": "User", "id": 5},
    )
    body = to_payload_update(cmd)["view"]
    assert body == {
        "title": "New",
        "all": _ALL,
        "any": _ANY,
        "description": "d",
        "active": True,
        "position": 7,
        "output": _OUTPUT,
        "restriction": {"type": "User", "id": 5},
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateViewCmd(active=False))["view"]
    assert body == {"active": False}


def test_update_converts_iterables_to_lists():
    body = to_payload_update(
        UpdateViewCmd(all=iter(_ALL), any=iter(_ANY))
    )["view"]
    assert body["all"] == _ALL
    assert body["any"] == _ANY
