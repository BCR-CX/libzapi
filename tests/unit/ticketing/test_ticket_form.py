import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketFormApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/ticket_forms", "ticket_forms"),
    ],
)
def test_ticket_form_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = TicketFormApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_ticket_form_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"ticket_form": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_form_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = TicketFormApiClient(https)
    client.get(88)

    https.get.assert_called_with("/api/v2/ticket_forms/88")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_ticket_form_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketFormApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
