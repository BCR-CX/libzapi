import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.domain.models.ticketing.ticket_metric import TicketMetric
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketMetricApiClient

ticket_metric_strategy = builds(
    TicketMetric,
    id=just(333),
)


@given(ticket_metric_strategy)
def test_ticket_metric_logical_key_from_id(audit):
    assert audit.logical_key.as_str() == "ticket_metric:metric_333"


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list_ticket", [999], "/api/v2/tickets/999/metrics", "ticket_metrics"),
    ],
)
def test_ticket_metric_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = TicketMetricApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_ticket_metric_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"ticket_metric": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_metric_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = TicketMetricApiClient(https)
    client.get(123)

    https.get.assert_called_with("/api/v2/ticket_metrics/123")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_ticket_metric_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketMetricApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_ticket(1))
