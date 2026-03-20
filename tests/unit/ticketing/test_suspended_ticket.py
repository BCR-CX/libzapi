import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.suspended_ticket import SuspendedTicket
from libzapi.infrastructure.api_clients.ticketing import SuspendedTicketApiClient

strategy = builds(
    SuspendedTicket,
    id=just(123),
)


@given(strategy)
def test_logical_key_from_id(suspended_ticket: SuspendedTicket):
    assert suspended_ticket.logical_key.as_str() == "suspended_ticket:id_123"


def test_suspended_ticket_api_client_get_one(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"suspended_ticket": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.suspended_ticket_api_client.to_domain",
        return_value=mocker.Mock(),  # does not matter what it is
    )

    client = SuspendedTicketApiClient(https)

    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/suspended_tickets/{fake_id}")


def test_suspended_ticket_api_client_list_all(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"suspended_tickets": []}

    client = SuspendedTicketApiClient(https)

    method = getattr(client, "list", None)
    list(method())

    https.get.assert_called_with("/api/v2/suspended_tickets")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_suspended_ticket_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = SuspendedTicketApiClient(https)

    with pytest.raises(error_cls):
        client.get(1)
