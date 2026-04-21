from datetime import datetime
from unittest.mock import Mock, sentinel

import pytest

from libzapi.application.commands.ticketing.group_cmds import (
    CreateGroupCmd,
    UpdateGroupCmd,
)
from libzapi.application.services.ticketing.groups_service import GroupsService
from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.domain.models.ticketing.group import Group
from libzapi.infrastructure.api_clients.ticketing import GroupApiClient
from libzapi.infrastructure.mappers.ticketing.group_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


# ---------------------------------------------------------------------------
# Domain / mapper
# ---------------------------------------------------------------------------


def test_mapper_to_domain_and_back_payload_roundtrip():
    raw = {
        "id": 301,
        "name": "Support Team",
        "description": "Handles customer support tickets",
        "is_public": True,
        "default": False,
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-02T12:00:00Z",
        "url": "https://example.zendesk.com/api/v2/groups/301.json",
        "deleted": False,
    }
    entity = to_domain(raw, Group)
    assert entity.id == 301
    assert entity.name == "Support Team"
    assert entity.description == "Handles customer support tickets"
    assert entity.is_public is True

    payload = to_payload_create(entity)
    assert payload == {
        "group": {
            "name": "Support Team",
            "description": "Handles customer support tickets",
            "is_public": True,
            "default": False,
        }
    }


def test_group_logical_key():
    group = Group(
        id=302,
        name="Engineering",
        description="Engineering Department",
        is_public=False,
        created_at=datetime.fromisoformat("2022-01-01T12:00:00Z"),
        updated_at=datetime.fromisoformat("2022-01-01T12:00:00Z"),
        url="https://example.zendesk.com/api/v2/groups/302.json",
        default=False,
        deleted=False,
    )
    assert group.logical_key.as_str() == "group:engineering"


# ---------------------------------------------------------------------------
# Mapper: to_payload_update branches
# ---------------------------------------------------------------------------


def test_update_payload_empty_cmd():
    assert to_payload_update(UpdateGroupCmd()) == {"group": {}}


def test_update_payload_all_fields():
    cmd = UpdateGroupCmd(name="n", description="d", is_public=True, default=False)
    assert to_payload_update(cmd) == {
        "group": {
            "name": "n",
            "description": "d",
            "is_public": True,
            "default": False,
        }
    }


def test_update_payload_preserves_false_booleans():
    cmd = UpdateGroupCmd(is_public=False, default=False)
    assert to_payload_update(cmd) == {
        "group": {"is_public": False, "default": False}
    }


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.group_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.mark.parametrize(
    "method, args, path",
    [
        ("list", (), "/api/v2/groups"),
        ("list_user", (42,), "/api/v2/users/42/groups"),
        ("list_assignable", (), "/api/v2/groups/assignable"),
    ],
)
def test_list_endpoints(method, args, path, http, domain):
    http.get.return_value = {"groups": []}
    client = GroupApiClient(http)
    list(getattr(client, method)(*args))
    http.get.assert_called_with(path)


@pytest.mark.parametrize(
    "method, args",
    [
        ("list", ()),
        ("list_user", (42,)),
        ("list_assignable", ()),
    ],
)
def test_list_yields_items(method, args, http, domain):
    http.get.return_value = {
        "groups": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = GroupApiClient(http)
    assert len(list(getattr(client, method)(*args))) == 2


def test_count_hits_endpoint(http):
    http.get.return_value = {
        "count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 3}
    }
    client = GroupApiClient(http)
    assert client.count().value == 3
    http.get.assert_called_with("/api/v2/groups/count")


def test_count_user_hits_endpoint(http):
    http.get.return_value = {
        "count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 2}
    }
    client = GroupApiClient(http)
    assert client.count_user(user_id=42).value == 2
    http.get.assert_called_with("/api/v2/users/42/groups/count")


def test_get_hits_endpoint(http, domain):
    http.get.return_value = {"group": {"id": 5}}
    client = GroupApiClient(http)
    client.get(group_id=5)
    http.get.assert_called_with("/api/v2/groups/5")


def test_count_assignable_hits_endpoint(http):
    http.get.return_value = {
        "count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 7}
    }
    client = GroupApiClient(http)
    snapshot = client.count_assignable()
    http.get.assert_called_with("/api/v2/groups/assignable/count")
    assert snapshot.value == 7


def test_create_posts_payload(http, domain):
    http.post.return_value = {"group": {"id": 1}}
    client = GroupApiClient(http)
    client.create(CreateGroupCmd(name="Acme"))
    http.post.assert_called_with(
        "/api/v2/groups",
        {
            "group": {
                "name": "Acme",
                "description": "",
                "is_public": False,
                "default": False,
            }
        },
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"group": {"id": 1}}
    client = GroupApiClient(http)
    client.update(group_id=1, entity=UpdateGroupCmd(name="x"))
    http.put.assert_called_with("/api/v2/groups/1", {"group": {"name": "x"}})


def test_delete_calls_endpoint(http):
    client = GroupApiClient(http)
    client.delete(group_id=5)
    http.delete.assert_called_with("/api/v2/groups/5")


# ---------------------------------------------------------------------------
# GroupsService
# ---------------------------------------------------------------------------


def _make_service():
    client = Mock()
    return GroupsService(client), client


class TestServiceDelegation:
    @pytest.mark.parametrize(
        "method, args, client_method, client_args",
        [
            ("list_all", (), "list", ()),
            ("list_user", (42,), "list_user", (42,)),
            ("list_assignable", (), "list_assignable", ()),
            ("count", (), "count", ()),
            ("count_user", (42,), "count_user", (42,)),
            ("count_assignable", (), "count_assignable", ()),
            ("get_by_id", (5,), "get", (5,)),
        ],
    )
    def test_delegates(self, method, args, client_method, client_args):
        service, client = _make_service()
        getattr(client, client_method).return_value = sentinel.result
        result = getattr(service, method)(*args)
        getattr(client, client_method).assert_called_once_with(*client_args)
        assert result is sentinel.result

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(5)


class TestServiceCreate:
    def test_builds_cmd_with_kwargs(self):
        service, client = _make_service()
        client.create.return_value = sentinel.group

        result = service.create(name="Acme", description="desc", is_public=True)

        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateGroupCmd)
        assert cmd.name == "Acme"
        assert cmd.description == "desc"
        assert cmd.is_public is True
        assert cmd.default is False
        assert result is sentinel.group

    def test_uses_defaults_when_only_name(self):
        service, client = _make_service()
        service.create(name="Acme")
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.description == ""
        assert cmd.is_public is False
        assert cmd.default is False


class TestServiceUpdate:
    def test_builds_cmd_with_kwargs(self):
        service, client = _make_service()
        client.update.return_value = sentinel.group

        result = service.update(7, name="New", description="d")

        call = client.update.call_args
        assert call.kwargs["group_id"] == 7
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, UpdateGroupCmd)
        assert cmd.name == "New"
        assert cmd.description == "d"
        assert result is sentinel.group

    def test_empty_kwargs_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(7)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.name is None


class TestServiceErrors:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_all_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(name="x")
