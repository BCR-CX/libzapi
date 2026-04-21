from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.infrastructure.mappers.ticketing.user_mapper import (
    to_payload_create,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_only_has_name():
    cmd = CreateUserCmd(name="alice")
    assert to_payload_create(cmd) == {"user": {"name": "alice"}}


def test_create_includes_optional_fields_when_set():
    cmd = CreateUserCmd(
        name="alice",
        email="a@x.y",
        role="agent",
        phone="+1",
        alias="ali",
        external_id="ext-1",
        organization_id=7,
        custom_role_id=3,
        default_group_id=4,
        details="d",
        notes="n",
        locale_id=1,
        time_zone="UTC",
        verified=True,
        active=True,
        moderator=False,
        only_private_comments=False,
        restricted_agent=False,
        suspended=False,
        ticket_restriction="assigned",
        user_fields={"k": "v"},
    )

    body = to_payload_create(cmd)["user"]
    assert body["name"] == "alice"
    assert body["email"] == "a@x.y"
    assert body["role"] == "agent"
    assert body["phone"] == "+1"
    assert body["alias"] == "ali"
    assert body["external_id"] == "ext-1"
    assert body["organization_id"] == 7
    assert body["custom_role_id"] == 3
    assert body["default_group_id"] == 4
    assert body["details"] == "d"
    assert body["notes"] == "n"
    assert body["locale_id"] == 1
    assert body["time_zone"] == "UTC"
    assert body["verified"] is True
    assert body["active"] is True
    assert body["moderator"] is False
    assert body["only_private_comments"] is False
    assert body["restricted_agent"] is False
    assert body["suspended"] is False
    assert body["ticket_restriction"] == "assigned"
    assert body["user_fields"] == {"k": "v"}


def test_create_tags_converted_to_list():
    cmd = CreateUserCmd(name="n", tags=("a", "b"))
    body = to_payload_create(cmd)["user"]
    assert body["tags"] == ["a", "b"]


def test_create_omits_none_fields():
    body = to_payload_create(CreateUserCmd(name="n"))["user"]
    assert list(body.keys()) == ["name"]


def test_create_preserves_false_boolean_values():
    body = to_payload_create(CreateUserCmd(name="n", verified=False))["user"]
    # verified=False must be preserved (None would be omitted, but False is a set value)
    assert body["verified"] is False


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_yields_empty_body():
    assert to_payload_update(UpdateUserCmd()) == {"user": {}}


def test_update_includes_name_when_set():
    body = to_payload_update(UpdateUserCmd(name="n"))["user"]
    assert body == {"name": "n"}


def test_update_omits_none_fields():
    body = to_payload_update(UpdateUserCmd(email="e@x.y"))["user"]
    assert body == {"email": "e@x.y"}


def test_update_tags_converted_to_list():
    body = to_payload_update(UpdateUserCmd(tags=("a", "b")))["user"]
    assert body["tags"] == ["a", "b"]


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateUserCmd(suspended=False))["user"]
    assert body == {"suspended": False}


def test_update_all_fields_together():
    cmd = UpdateUserCmd(
        name="n",
        email="e@x.y",
        role="agent",
        phone="+1",
        alias="a",
        external_id="ext",
        organization_id=1,
        custom_role_id=2,
        default_group_id=3,
        details="d",
        notes="x",
        locale_id=4,
        time_zone="UTC",
        verified=True,
        active=True,
        moderator=True,
        only_private_comments=True,
        restricted_agent=True,
        suspended=True,
        ticket_restriction="organization",
        tags=["a"],
        user_fields={"k": 1},
    )
    body = to_payload_update(cmd)["user"]
    assert body["name"] == "n"
    assert body["ticket_restriction"] == "organization"
    assert body["tags"] == ["a"]
    assert body["user_fields"] == {"k": 1}
