import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import UserFieldApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list_all", [], "/api/v2/user_fields", "user_fields"),
        ("list_options", [33], "/api/v2/user_fields/33/options", "custom_field_options"),
    ],
)
def test_user_field_api_client(method_name, args, expected_path, return_value, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: []}

    client = UserFieldApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_user_field_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"user_field": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_field_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = UserFieldApiClient(https)
    client.get(44)

    https.get.assert_called_with("/api/v2/user_fields/44")


def test_user_field_api_client_get_option(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_field_option": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.user_field_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = UserFieldApiClient(https)
    client.get_option(44, 55)

    https.get.assert_called_with("/api/v2/user_fields/44/options/55")


def test_user_field_logical_key_normalises_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.user_field import UserField

    field = UserField(
        id=1,
        url="https://x",
        type="text",
        key="Account Region",
        title="Region",
        description="",
        raw_description="",
        position=1,
        active=True,
        system=False,
        regexp_for_validation=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert field.logical_key.as_str() == "user_field:account_region"


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_user_field_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = UserFieldApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all())
