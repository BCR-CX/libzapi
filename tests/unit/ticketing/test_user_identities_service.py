import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)
from libzapi.application.services.ticketing.user_identities_service import (
    UserIdentitiesService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return UserIdentitiesService(client), client


class TestDelegation:
    def test_list_for_user_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.iter
        assert service.list_for_user(42) is sentinel.iter
        client.list.assert_called_once_with(42)

    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.identity
        assert service.get_by_id(3, 9) is sentinel.identity
        client.get.assert_called_once_with(user_id=3, identity_id=9)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(3, 9)
        client.delete.assert_called_once_with(user_id=3, identity_id=9)

    def test_make_primary_delegates(self):
        service, client = _make_service()
        client.make_primary.return_value = sentinel.list_
        assert service.make_primary(3, 9) is sentinel.list_
        client.make_primary.assert_called_once_with(user_id=3, identity_id=9)

    def test_verify_delegates(self):
        service, client = _make_service()
        client.verify.return_value = sentinel.identity
        assert service.verify(3, 9) is sentinel.identity
        client.verify.assert_called_once_with(user_id=3, identity_id=9)

    def test_request_verification_delegates(self):
        service, client = _make_service()
        service.request_verification(3, 9)
        client.request_verification.assert_called_once_with(
            user_id=3, identity_id=9
        )


class TestCreate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.identity
        result = service.create(
            user_id=3,
            type="email",
            value="x@y.com",
            verified=True,
            primary=False,
        )
        call = client.create.call_args
        assert call.kwargs["user_id"] == 3
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateUserIdentityCmd)
        assert cmd.type == "email"
        assert cmd.value == "x@y.com"
        assert cmd.verified is True
        assert cmd.primary is False
        assert result is sentinel.identity

    def test_defaults_omitted_are_none(self):
        service, client = _make_service()
        service.create(user_id=3, type="email", value="x@y.com")
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.verified is None
        assert cmd.primary is None


class TestUpdate:
    def test_builds_cmd_with_kwargs(self):
        service, client = _make_service()
        client.update.return_value = sentinel.identity
        service.update(3, 9, value="new@y.com", verified=True)
        call = client.update.call_args
        assert call.kwargs["user_id"] == 3
        assert call.kwargs["identity_id"] == 9
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateUserIdentityCmd)
        assert cmd.value == "new@y.com"
        assert cmd.verified is True

    def test_empty_kwargs_builds_empty_cmd(self):
        service, client = _make_service()
        service.update(3, 9)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.value is None
        assert cmd.verified is None


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_get_propagates_error(self, error_cls):
        service, client = _make_service()
        client.get.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.get_by_id(1, 2)
