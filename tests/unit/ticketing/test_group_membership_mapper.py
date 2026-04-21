from libzapi.application.commands.ticketing.group_membership_cmds import (
    CreateGroupMembershipCmd,
)
from libzapi.infrastructure.mappers.ticketing.group_membership_mapper import (
    to_payload_create,
)


def test_create_minimum_payload():
    payload = to_payload_create(CreateGroupMembershipCmd(user_id=1, group_id=2))
    assert payload == {"group_membership": {"user_id": 1, "group_id": 2}}


def test_create_with_default_flag():
    payload = to_payload_create(
        CreateGroupMembershipCmd(user_id=1, group_id=2, default=True)
    )
    assert payload == {
        "group_membership": {"user_id": 1, "group_id": 2, "default": True}
    }


def test_create_omits_default_when_none():
    payload = to_payload_create(
        CreateGroupMembershipCmd(user_id=1, group_id=2, default=None)
    )
    assert "default" not in payload["group_membership"]


def test_create_coerces_ids_to_int():
    payload = to_payload_create(
        CreateGroupMembershipCmd(user_id="1", group_id="2")  # type: ignore[arg-type]
    )
    body = payload["group_membership"]
    assert isinstance(body["user_id"], int)
    assert isinstance(body["group_id"], int)
