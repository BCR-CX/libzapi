import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.address import Address
from libzapi.infrastructure.api_clients.voice.address_api_client import AddressApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.address_api_client"

strategy = builds(Address, id=just(1))


@given(strategy)
def test_logical_key(model: Address) -> None:
    assert model.logical_key.as_str() == "address:1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"addresses": [{}]}
    client = AddressApiClient(https)
    list(client.list_all())
    https.get.assert_called_with("/api/v2/channels/voice/addresses")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"address": {}}
    client = AddressApiClient(https)
    client.get(1)
    https.get.assert_called_with("/api/v2/channels/voice/addresses/1")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"address": {"name": "a"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"address": {}}
    client = AddressApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/channels/voice/addresses", json={"address": {"name": "a"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"address": {"name": "u"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"address": {}}
    client = AddressApiClient(https)
    client.update(1, mocker.Mock())
    https.put.assert_called_with("/api/v2/channels/voice/addresses/1", json={"address": {"name": "u"}})


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = AddressApiClient(https)
    client.delete(1)
    https.delete.assert_called_with("/api/v2/channels/voice/addresses/1")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = AddressApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_all())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = AddressApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"address": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")
    client = AddressApiClient(https)
    with pytest.raises(error_cls):
        client.create(mocker.Mock())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")
    client = AddressApiClient(https)
    with pytest.raises(error_cls):
        client.delete(1)
