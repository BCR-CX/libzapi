import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.domain.models.ticketing.ticket_trigger_category import TicketTriggerCategory
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import TicketTriggerCategoryApiClient

strategy = builds(
    TicketTriggerCategory,
    name=just("CAT V"),
)


@given(strategy)
def test_trigger_category_logical_key_from_name(model: TicketTriggerCategory):
    assert model.logical_key.as_str() == "ticket_trigger_category:cat_v"


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list", [], "/api/v2/trigger_categories", "trigger_categories"),
    ],
)
def test_trigger_category_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = TicketTriggerCategoryApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_trigger_category_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"trigger_category": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.ticket_trigger_category_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = TicketTriggerCategoryApiClient(https)
    client.get(66)

    https.get.assert_called_with("/api/v2/trigger_categories/66")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_trigger_category_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = TicketTriggerCategoryApiClient(https)

    with pytest.raises(error_cls):
        list(client.list())
