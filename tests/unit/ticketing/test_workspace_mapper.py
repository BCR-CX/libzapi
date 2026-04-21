from libzapi.application.commands.ticketing.workspace_cmds import (
    CreateWorkspaceCmd,
    UpdateWorkspaceCmd,
)
from libzapi.infrastructure.mappers.ticketing.workspace_mapper import (
    to_payload_create,
    to_payload_update,
)


_COND = {"all": [{"field": "status", "operator": "is", "value": "new"}]}


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(CreateWorkspaceCmd(title="W", conditions=_COND))
    assert payload == {
        "workspace": {"title": "W", "conditions": _COND}
    }


def test_create_includes_all_optional_fields():
    cmd = CreateWorkspaceCmd(
        title="W",
        conditions=_COND,
        description="desc",
        activated=True,
        prefer_workspace_app_order=True,
        macros=[1, 2],
        apps=[{"id": 1, "expand": True, "position": 1}],
        ticket_form_id=9,
        position=2,
    )

    body = to_payload_create(cmd)["workspace"]

    assert body["title"] == "W"
    assert body["conditions"] == _COND
    assert body["description"] == "desc"
    assert body["activated"] is True
    assert body["prefer_workspace_app_order"] is True
    assert body["macros"] == [1, 2]
    assert body["apps"] == [{"id": 1, "expand": True, "position": 1}]
    assert body["ticket_form_id"] == 9
    assert body["position"] == 2


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateWorkspaceCmd(
            title="W",
            conditions=_COND,
            activated=False,
            prefer_workspace_app_order=False,
        )
    )["workspace"]
    assert body["activated"] is False
    assert body["prefer_workspace_app_order"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateWorkspaceCmd(title="W", conditions=_COND)
    )["workspace"]
    assert set(body.keys()) == {"title", "conditions"}


def test_create_converts_iterables_to_lists():
    body = to_payload_create(
        CreateWorkspaceCmd(
            title="W",
            conditions=_COND,
            macros=iter([7]),
            apps=iter([{"id": 1}]),
        )
    )["workspace"]
    assert body["macros"] == [7]
    assert body["apps"] == [{"id": 1}]


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateWorkspaceCmd()) == {"workspace": {}}


def test_update_includes_all_fields():
    cmd = UpdateWorkspaceCmd(
        title="W2",
        conditions=_COND,
        description="d",
        activated=True,
        prefer_workspace_app_order=True,
        macros=[1],
        apps=[{"id": 3}],
        ticket_form_id=9,
        position=1,
    )
    body = to_payload_update(cmd)["workspace"]
    assert body == {
        "title": "W2",
        "conditions": _COND,
        "description": "d",
        "activated": True,
        "prefer_workspace_app_order": True,
        "macros": [1],
        "apps": [{"id": 3}],
        "ticket_form_id": 9,
        "position": 1,
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateWorkspaceCmd(activated=False))["workspace"]
    assert body == {"activated": False}


def test_update_converts_iterables_to_lists():
    body = to_payload_update(
        UpdateWorkspaceCmd(macros=iter([7]), apps=iter([{"id": 1}]))
    )["workspace"]
    assert body["macros"] == [7]
    assert body["apps"] == [{"id": 1}]
