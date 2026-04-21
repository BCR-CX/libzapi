import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)
from libzapi.application.services.ticketing.sla_policies_service import (
    SlaPoliciesService,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


_FILTER = {"all": [], "any": []}
_METRICS = [
    {
        "priority": "low",
        "metric": "first_reply_time",
        "target": 480,
        "business_hours": False,
    }
]


def _make_service(client=None):
    client = client or Mock()
    return SlaPoliciesService(client), client


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.items
        assert service.list() is sentinel.items

    def test_list_definitions_delegates(self):
        service, client = _make_service()
        client.list_definitions.return_value = {"x": 1}
        assert service.list_definitions() == {"x": 1}

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.item
        assert service.get(5) is sentinel.item
        client.get.assert_called_once_with(sla_policy_id=5)

    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(5)
        client.delete.assert_called_once_with(sla_policy_id=5)

    def test_reorder_delegates(self):
        service, client = _make_service()
        client.reorder.return_value = sentinel.reordered
        assert service.reorder([1, 2]) is sentinel.reordered
        client.reorder.assert_called_once_with(sla_policy_ids=[1, 2])


class TestCreate:
    def test_builds_create_cmd_and_delegates(self):
        service, client = _make_service()
        client.create.return_value = sentinel.item
        result = service.create(
            title="T", filter=_FILTER, policy_metrics=_METRICS
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateSlaPolicyCmd)
        assert cmd.title == "T"
        assert cmd.filter == _FILTER
        assert cmd.policy_metrics == _METRICS
        assert result is sentinel.item

    def test_passes_all_optional_fields(self):
        service, client = _make_service()
        service.create(
            title="T",
            filter=_FILTER,
            policy_metrics=_METRICS,
            description="d",
            position=3,
        )
        cmd = client.create.call_args.kwargs["entity"]
        assert cmd.description == "d"
        assert cmd.position == 3


class TestUpdate:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update.return_value = sentinel.item
        result = service.update(7, description="updated")
        assert client.update.call_args.kwargs["sla_policy_id"] == 7
        cmd = client.update.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateSlaPolicyCmd)
        assert cmd.description == "updated"
        assert result is sentinel.item

    def test_empty_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update(1)
        cmd = client.update.call_args.kwargs["entity"]
        assert cmd.title is None


class TestErrorPropagation:
    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create(
                title="t", filter=_FILTER, policy_metrics=_METRICS
            )

    @pytest.mark.parametrize(
        "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
    )
    def test_update_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.update.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.update(1)

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list()
