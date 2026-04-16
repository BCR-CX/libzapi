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


MODULE = "libzapi.infrastructure.api_clients.custom_data.custom_object"


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"custom_object": {"key": "car"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"custom_object": {}}
    client = CustomObjectApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects", json={"custom_object": {"key": "car"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"custom_object": {"title": "Car"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"custom_object": {}}
    client = CustomObjectApiClient(https)
    client.update("car", mocker.Mock())
    https.patch.assert_called_with("/api/v2/custom_objects/car", json={"custom_object": {"title": "Car"}})


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = CustomObjectApiClient(https)
    client.delete("car")
    https.delete.assert_called_with("/api/v2/custom_objects/car")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.post.side_effect = error_cls("error")
    client = CustomObjectApiClient(https)
    with pytest.raises(error_cls):
        client.create(mocker.Mock())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_update_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.patch.side_effect = error_cls("error")
    client = CustomObjectApiClient(https)
    with pytest.raises(error_cls):
        client.update("car", mocker.Mock())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.delete.side_effect = error_cls("error")
    client = CustomObjectApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car")
