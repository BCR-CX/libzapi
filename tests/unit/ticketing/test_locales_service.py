import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.locales_service import LocalesService
from libzapi.domain.errors import Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return LocalesService(client), client


class TestDelegation:
    def test_list_all_delegates(self):
        service, client = _make_service()
        client.list_all.return_value = sentinel.items
        assert service.list_all() is sentinel.items
        client.list_all.assert_called_once_with()

    def test_list_agent_delegates(self):
        service, client = _make_service()
        service.list_agent()
        client.list_agent.assert_called_once_with()

    def test_list_public_delegates(self):
        service, client = _make_service()
        service.list_public()
        client.list_public.assert_called_once_with()

    def test_get_delegates(self):
        service, client = _make_service()
        service.get(1)
        client.get.assert_called_once_with(locale_id_or_code=1)

    def test_get_current_delegates(self):
        service, client = _make_service()
        service.get_current()
        client.get_current.assert_called_once_with()

    def test_detect_best_delegates(self):
        service, client = _make_service()
        service.detect_best(["en-US"])
        client.detect_best.assert_called_once_with(available=["en-US"])


def test_propagates_unauthorized():
    service, client = _make_service()
    client.list_all.side_effect = Unauthorized("x")
    with pytest.raises(Unauthorized):
        service.list_all()
