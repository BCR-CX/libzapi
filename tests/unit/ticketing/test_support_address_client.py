import pytest

from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)
from libzapi.infrastructure.api_clients.ticketing.support_address_api_client import (
    SupportAddressApiClient,
)


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.support_address_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


@pytest.fixture
def yield_items(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.support_address_api_client.yield_items"
    )


def test_list_yields_items(http, domain, yield_items):
    yield_items.return_value = iter([{"id": 1}, {"id": 2}])
    client = SupportAddressApiClient(http)
    result = list(client.list())
    assert [r["id"] for r in result] == [1, 2]
    assert all(r["_cls"] == "RecipientAddress" for r in result)
    kwargs = yield_items.call_args.kwargs
    assert kwargs["first_path"] == "/api/v2/recipient_addresses"
    assert kwargs["items_key"] == "recipient_addresses"


def test_get_reads_recipient_address_key(http, domain):
    http.get.return_value = {"recipient_address": {"id": 7, "name": "N"}}
    client = SupportAddressApiClient(http)
    result = client.get(support_address_id=7)
    http.get.assert_called_with("/api/v2/recipient_addresses/7")
    assert result["_cls"] == "RecipientAddress"
    assert result["name"] == "N"


def test_create_posts_payload(http, domain):
    http.post.return_value = {"recipient_address": {"id": 1, "email": "x@x"}}
    client = SupportAddressApiClient(http)
    result = client.create(CreateSupportAddressCmd(email="x@x"))
    http.post.assert_called_with(
        "/api/v2/recipient_addresses",
        {"recipient_address": {"email": "x@x"}},
    )
    assert result["_cls"] == "RecipientAddress"


def test_update_puts_payload(http, domain):
    http.put.return_value = {"recipient_address": {"id": 1, "name": "N"}}
    client = SupportAddressApiClient(http)
    client.update(
        support_address_id=1, entity=UpdateSupportAddressCmd(name="N")
    )
    http.put.assert_called_with(
        "/api/v2/recipient_addresses/1", {"recipient_address": {"name": "N"}}
    )


def test_delete_calls_delete(http):
    client = SupportAddressApiClient(http)
    client.delete(support_address_id=9)
    http.delete.assert_called_with("/api/v2/recipient_addresses/9")


def test_verify_puts_empty_body(http):
    http.put.return_value = {"status": "ok"}
    client = SupportAddressApiClient(http)
    result = client.verify(support_address_id=3)
    http.put.assert_called_with("/api/v2/recipient_addresses/3/verify", {})
    assert result == {"status": "ok"}
