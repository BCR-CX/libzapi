from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)
from libzapi.infrastructure.mappers.ticketing.user_identity_mapper import (
    to_payload_create,
    to_payload_update,
)


def test_create_minimal():
    cmd = CreateUserIdentityCmd(type="email", value="x@y.com")
    assert to_payload_create(cmd) == {
        "identity": {"type": "email", "value": "x@y.com"}
    }


def test_create_with_verified_true():
    cmd = CreateUserIdentityCmd(type="email", value="x@y.com", verified=True)
    assert to_payload_create(cmd)["identity"]["verified"] is True


def test_create_with_verified_false():
    cmd = CreateUserIdentityCmd(type="email", value="x@y.com", verified=False)
    assert to_payload_create(cmd)["identity"]["verified"] is False


def test_create_with_primary_true():
    cmd = CreateUserIdentityCmd(type="email", value="x@y.com", primary=True)
    assert to_payload_create(cmd)["identity"]["primary"] is True


def test_create_with_primary_false():
    cmd = CreateUserIdentityCmd(type="email", value="x@y.com", primary=False)
    assert to_payload_create(cmd)["identity"]["primary"] is False


def test_update_empty():
    cmd = UpdateUserIdentityCmd()
    assert to_payload_update(cmd) == {"identity": {}}


def test_update_value_only():
    cmd = UpdateUserIdentityCmd(value="new@y.com")
    assert to_payload_update(cmd) == {"identity": {"value": "new@y.com"}}


def test_update_verified_only():
    cmd = UpdateUserIdentityCmd(verified=True)
    assert to_payload_update(cmd) == {"identity": {"verified": True}}


def test_update_verified_false():
    cmd = UpdateUserIdentityCmd(verified=False)
    assert to_payload_update(cmd)["identity"]["verified"] is False


def test_update_both():
    cmd = UpdateUserIdentityCmd(value="new@y.com", verified=True)
    assert to_payload_update(cmd) == {
        "identity": {"value": "new@y.com", "verified": True}
    }
