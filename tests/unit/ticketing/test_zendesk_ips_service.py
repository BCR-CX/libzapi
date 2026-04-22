import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.ticketing.zendesk_ips_service import ZendeskIPsService
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return ZendeskIPsService(client), client


def test_get_current_delegates_to_client():
    service, client = _make_service()
    client.get.return_value = sentinel.ips
    assert service.get_current() is sentinel.ips
    client.get.assert_called_once_with()


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_get_current_propagates_error(error_cls):
    service, client = _make_service()
    client.get.side_effect = error_cls("boom")
    with pytest.raises(error_cls):
        service.get_current()
