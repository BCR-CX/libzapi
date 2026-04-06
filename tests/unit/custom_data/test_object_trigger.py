import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.custom_data.object_trigger import ObjectTrigger
from libzapi.infrastructure.api_clients.custom_data.object_trigger import ObjectTriggerApiClient

MODULE = "libzapi.infrastructure.api_clients.custom_data.object_trigger"

strategy = builds(ObjectTrigger, id=just(42), title=just("Test"))


@given(strategy)
def test_logical_key(model: ObjectTrigger):
    assert model.logical_key.as_str() == "object_trigger:42"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"triggers": [{}]}
    client = ObjectTriggerApiClient(https)
    list(client.list_all("car"))
    https.get.assert_called_with("/api/v2/custom_objects/car/triggers")


def test_list_active_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"triggers": [{}]}
    client = ObjectTriggerApiClient(https)
    list(client.list_active("car"))
    https.get.assert_called_with("/api/v2/custom_objects/car/triggers/active")


def test_search_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"triggers": [{}]}
    client = ObjectTriggerApiClient(https)
    list(client.search("car", "test"))
    https.get.assert_called_with("/api/v2/custom_objects/car/triggers/search?query=test")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"trigger": {}}
    client = ObjectTriggerApiClient(https)
    client.get("car", 42)
    https.get.assert_called_with("/api/v2/custom_objects/car/triggers/42")


def test_definitions_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"definitions": {}}
    client = ObjectTriggerApiClient(https)
    client.definitions("car")
    https.get.assert_called_with("/api/v2/custom_objects/car/triggers/definitions")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"trigger": {"title": "T"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"trigger": {}}
    client = ObjectTriggerApiClient(https)
    client.create("car", mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects/car/triggers", json={"trigger": {"title": "T"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"trigger": {"title": "U"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"trigger": {}}
    client = ObjectTriggerApiClient(https)
    client.update("car", 42, mocker.Mock())
    https.put.assert_called_with("/api/v2/custom_objects/car/triggers/42", json={"trigger": {"title": "U"}})


def test_update_many_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update_many", return_value={"triggers": [{"id": 1}]})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"triggers": [{}]}
    client = ObjectTriggerApiClient(https)
    client.update_many("car", mocker.Mock())
    https.put.assert_called_with("/api/v2/custom_objects/car/triggers/update_many", json={"triggers": [{"id": 1}]})


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ObjectTriggerApiClient(https)
    client.delete("car", 42)
    https.delete.assert_called_with("/api/v2/custom_objects/car/triggers/42")


def test_delete_many_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = ObjectTriggerApiClient(https)
    client.delete_many("car", [1, 2, 3])
    https.delete.assert_called_with("/api/v2/custom_objects/car/triggers/destroy_many?ids=1,2,3")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = ObjectTriggerApiClient(https)
    with pytest.raises(error_cls):
        client.get("car", 42)


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
    client = ObjectTriggerApiClient(https)
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
    client = ObjectTriggerApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car", 42)
