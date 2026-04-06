import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.custom_data.custom_object_field import CustomObjectFieldApiClient


@pytest.mark.parametrize(
    "method_name, args, expected_path, return_value",
    [
        (
            "list_all",
            ["car"],
            "/api/v2/custom_objects/car/fields",
            "custom_object_fields",
        ),
    ],
)
def test_custom_object_field_api_client(method_name, args, expected_path, return_value, mocker):
    mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object_field.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {return_value: [{}]}

    client = CustomObjectFieldApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object_field.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_field": {"key": "make"}}

    client = CustomObjectFieldApiClient(https)
    client.get("car", 123)

    https.get.assert_called_with("/api/v2/custom_objects/car/fields/123")
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
def test_custom_object_field_api_client_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectFieldApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("car"))


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_custom_object_field_api_client_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectFieldApiClient(https)

    with pytest.raises(error_cls):
        client.get("car", 123)


MODULE = "libzapi.infrastructure.api_clients.custom_data.custom_object_field"


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"custom_object_field": {"key": "make"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"custom_object_field": {}}
    client = CustomObjectFieldApiClient(https)
    client.create("car", mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects/car/fields", json={"custom_object_field": {"key": "make"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"custom_object_field": {"title": "Make"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"custom_object_field": {}}
    client = CustomObjectFieldApiClient(https)
    client.update("car", 123, mocker.Mock())
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/fields/123", json={"custom_object_field": {"title": "Make"}}
    )


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = CustomObjectFieldApiClient(https)
    client.delete("car", 123)
    https.delete.assert_called_with("/api/v2/custom_objects/car/fields/123")


def test_reorder_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_payload_reorder", return_value={"field_ids": [3, 1, 2]})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {}
    client = CustomObjectFieldApiClient(https)
    client.reorder("car", [3, 1, 2])
    https.put.assert_called_with("/api/v2/custom_objects/car/fields/reorder", json={"field_ids": [3, 1, 2]})


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
    client = CustomObjectFieldApiClient(https)
    with pytest.raises(error_cls):
        client.create("car", mocker.Mock())


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
    client = CustomObjectFieldApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car", 123)
