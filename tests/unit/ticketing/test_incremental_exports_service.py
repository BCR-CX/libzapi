import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.incremental_exports_service import (
    IncrementalExportsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return IncrementalExportsService(client), client


class TestDelegation:
    @pytest.mark.parametrize(
        "method, client_method",
        [
            ("tickets", "tickets"),
            ("tickets_cursor", "tickets_cursor"),
            ("ticket_events", "ticket_events"),
            ("users", "users"),
            ("users_cursor", "users_cursor"),
            ("organizations", "organizations"),
        ],
    )
    def test_method_delegates(self, method, client_method):
        service, client = _make_service()
        getattr(client, client_method).return_value = sentinel.result
        result = getattr(service, method)(start_time=100)
        getattr(client, client_method).assert_called_once_with(start_time=100)
        assert result is sentinel.result


class TestSample:
    def test_delegates(self):
        service, client = _make_service()
        client.sample.return_value = sentinel.sample
        result = service.sample(resource="tickets", start_time=200)
        client.sample.assert_called_once_with(resource="tickets", start_time=200)
        assert result is sentinel.sample


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_tickets_propagates_error(self, error_cls):
        service, client = _make_service()
        client.tickets.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.tickets(start_time=1)
