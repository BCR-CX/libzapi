import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import AutomationApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list_all", [], "/api/v2/automations", "automations"),
        ("list_active", [], "/api/v2/automations/active", "automations"),
    ],
)
def test_automation_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = AutomationApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_automation_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"automation": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.automation_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = AutomationApiClient(https)
    client.get(42)

    https.get.assert_called_with("/api/v2/automations/42")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_automation_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AutomationApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all())
