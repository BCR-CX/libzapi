import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.greeting import Greeting, GreetingCategory
from libzapi.infrastructure.api_clients.voice.greeting_api_client import GreetingApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.greeting_api_client"

greeting_strategy = builds(Greeting, id=just("1"))
category_strategy = builds(GreetingCategory, id=just(1))


@given(greeting_strategy)
def test_greeting_logical_key(model: Greeting) -> None:
    assert model.logical_key.as_str() == "greeting:1"


@given(category_strategy)
def test_greeting_category_logical_key(model: GreetingCategory) -> None:
    assert model.logical_key.as_str() == "greeting_category:1"


def test_list_all_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"greetings": []}
    client = GreetingApiClient(https)
    list(client.list_all())
    https.get.assert_called_with("/api/v2/channels/voice/greetings")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"greeting": {}}
    client = GreetingApiClient(https)
    client.get(1)
    https.get.assert_called_with("/api/v2/channels/voice/greetings/1")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"greeting": {"name": "g"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"greeting": {}}
    client = GreetingApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/channels/voice/greetings", json={"greeting": {"name": "g"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"greeting": {"name": "u"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"greeting": {}}
    client = GreetingApiClient(https)
    client.update(1, mocker.Mock())
    https.put.assert_called_with("/api/v2/channels/voice/greetings/1", json={"greeting": {"name": "u"}})


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = GreetingApiClient(https)
    client.delete(1)
    https.delete.assert_called_with("/api/v2/channels/voice/greetings/1")


def test_list_categories_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"greeting_categories": [{}]}
    client = GreetingApiClient(https)
    list(client.list_categories())
    https.get.assert_called_with("/api/v2/channels/voice/greeting_categories")


def test_get_category_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"greeting_category": {}}
    client = GreetingApiClient(https)
    client.get_category(1)
    https.get.assert_called_with("/api/v2/channels/voice/greeting_categories/1")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = GreetingApiClient(https)
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
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = GreetingApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)


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
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"greeting": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")
    client = GreetingApiClient(https)
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
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")
    client = GreetingApiClient(https)
    with pytest.raises(error_cls):
        client.delete(1)
