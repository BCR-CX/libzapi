import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.group_membership_cmds import (
    CreateGroupMembershipCmd,
)
from libzapi.application.services.ticketing.group_memberships_service import (
    GroupMembershipsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return GroupMembershipsService(client), client


class TestDelegation:
    @pytest.mark.parametrize(
        "method, args, client_method, client_args",
        [
            ("list_all", (), "list", ()),
            ("list_by_user", (42,), "list_by_user", (42,)),
            ("list_by_group", (7,), "list_by_group", (7,)),
            ("list_assignable", (7,), "list_assignable", (7,)),
            (
                "list_assignable_for_user",
                (42,),
                "list_assignable_for_user",
                (42,),
            ),
            ("get_by_id", (5,), "get", (5,)),
            ("get_for_user", (3, 5), "get_for_user", (3, 5)),
            ("make_default", (3, 9), "make_default", (3, 9)),
        ],
    )
    def test_method_delegates(self, method, args, client_method, client_args):
        service, client = _make_service()
        getattr(client, client_method).return_value = sentinel.result

        result = getattr(service, method)(*args)

        getattr(client, client_method).assert_called_once_with(*client_args)
        assert result is sentinel.result

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(9)
        client.delete.assert_called_once_with(9)

    def test_delete_for_user_delegates(self):
        service, client = _make_service()
        service.delete_for_user(3, 9)
        client.delete_for_user.assert_called_once_with(3, 9)


class TestCreate:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.gm

        result = service.create(user_id=3, group_id=4, default=True)

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateGroupMembershipCmd)
        assert cmd.user_id == 3
        assert cmd.group_id == 4
        assert cmd.default is True
        assert result is sentinel.gm

    def test_default_omitted_builds_cmd_with_none(self):
        service, client = _make_service()
        service.create(user_id=3, group_id=4)
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.default is None


class TestCreateForUser:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create_for_user.return_value = sentinel.gm

        result = service.create_for_user(user_id=3, group_id=4)

        call = client.create_for_user.call_args
        assert call.kwargs["user_id"] == 3
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateGroupMembershipCmd)
        assert cmd.user_id == 3
        assert cmd.group_id == 4
        assert result is sentinel.gm


class TestCreateMany:
    def test_converts_dicts_to_commands(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.job

        result = service.create_many(
            [
                {"user_id": 1, "group_id": 2},
                {"user_id": 3, "group_id": 4, "default": True},
            ]
        )

        entities = client.create_many.call_args.kwargs["entities"]
        assert all(isinstance(c, CreateGroupMembershipCmd) for c in entities)
        assert entities[0].user_id == 1
        assert entities[1].default is True
        assert result is sentinel.job

    def test_empty_input(self):
        service, client = _make_service()
        service.create_many([])
        assert client.create_many.call_args.kwargs["entities"] == []


class TestDestroyMany:
    def test_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(membership_ids=[1, 2])


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(user_id=1, group_id=2)
