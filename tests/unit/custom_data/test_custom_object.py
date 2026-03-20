import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.custom_data.custom_object import CustomObjectApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        ("list_all", [], "/api/v2/custom_objects", "custom_objects"),
    ],
)
def test_custom_object_api_client(method_name, args, expected_path, return_value, mocker):
    mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: [{}]}

    client = CustomObjectApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object": {"key": "car"}}

    client = CustomObjectApiClient(https)
    client.get("car")

    https.get.assert_called_with("/api/v2/custom_objects/car")
    mock_to_domain.assert_called_once()


def test_limit_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"count": 5, "limit": 50}

    client = CustomObjectApiClient(https)
    client.limit()

    https.get.assert_called_with("/api/v2/custom_objects/limits/object_limit")
    mock_to_domain.assert_called_once()


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_custom_object_api_client_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectApiClient(https)

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
def test_custom_object_api_client_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectApiClient(https)

    with pytest.raises(error_cls):
        client.get("car")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_custom_object_api_client_limit_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectApiClient(https)

    with pytest.raises(error_cls):
        client.limit()
