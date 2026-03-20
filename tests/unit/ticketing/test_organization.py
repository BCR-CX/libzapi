import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import OrganizationApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/organizations", "organizations"),
        ("list_organizations", [456], "/api/v2/users/456/organizations", "organizations"),
    ],
)
def test_organization_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = OrganizationApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_organization_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organization": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.organization_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = OrganizationApiClient(https)
    client.get(99)

    https.get.assert_called_with("/api/v2/organizations/99")


def test_organization_api_client_search_by_external_id(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organizations": []}

    client = OrganizationApiClient(https)
    list(client.search(external_id="ext_123"))

    https.get.assert_called_with("/api/v2/organizations/search?external_id=ext_123")


def test_organization_api_client_search_by_name(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"organizations": []}

    client = OrganizationApiClient(https)
    list(client.search(name="Acme"))

    https.get.assert_called_with("/api/v2/organizations/search?name=Acme")


def test_organization_api_client_search_raises_without_params():
    client = OrganizationApiClient(None)

    with pytest.raises(ValueError, match="Either external_id or name must be provided"):
        list(client.search())


def test_organization_api_client_count(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"count": {"refreshed_at": "2024-01-01T00:00:00Z", "value": 42}}

    client = OrganizationApiClient(https)
    result = client.count()

    https.get.assert_called_with("/api/v2/organizations/count")
    assert result.value == 42


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_organization_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = OrganizationApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
