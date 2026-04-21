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


def test_ticket_form_logical_key_normalises_raw_name():
    from datetime import datetime

    from libzapi.domain.models.ticketing.ticket_form import TicketForm

    form = TicketForm(
        id=1,
        raw_name="Default Form",
        raw_display_name="Default",
        end_user_visible=True,
        position=1,
        ticket_field_ids=[],
        active=True,
        default=True,
        in_all_brands=True,
        restricted_brand_ids=[],
        url="https://x",
        name="Default Form",
        display_name="Default",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert form.logical_key.as_str() == "ticket_form:default_form"


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
