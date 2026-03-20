import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import BrandAgentApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/brand_agents", "brand_agents"),
        ("list_by_agent", [101], "/api/v2/users/101/brand_agents", "brand_agents"),
        ("list_by_brand", [202], "/api/v2/brands/202/agents", "brand_agents"),
    ],
)
def test_brand_agent_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = BrandAgentApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_brand_agent_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"brand_agent": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.brand_agent_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = BrandAgentApiClient(https)
    client.get(55)

    https.get.assert_called_with("/api/v2/brand_agents/55")


def test_brand_agent_api_client_get_membership(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"brand_agent": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.brand_agent_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = BrandAgentApiClient(https)
    client.get_brand_agent_membership(10, 20)

    https.get.assert_called_with("/api/v2/users/10/brand_agents/20")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_brand_agent_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = BrandAgentApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
