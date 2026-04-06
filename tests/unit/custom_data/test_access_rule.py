import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.custom_data.access_rule import AccessRule
from libzapi.infrastructure.api_clients.custom_data.access_rule import AccessRuleApiClient

MODULE = "libzapi.infrastructure.api_clients.custom_data.access_rule"

strategy = builds(AccessRule, id=just("rule-1"))


@given(strategy)
def test_logical_key(model: AccessRule):
    assert model.logical_key.as_str() == "access_rule:rule-1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"access_rules": [{}]}
    client = AccessRuleApiClient(https)
    list(client.list_all("car"))
    https.get.assert_called_with("/api/v2/custom_objects/car/access_rules")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"access_rule": {}}
    client = AccessRuleApiClient(https)
    client.get("car", "rule-1")
    https.get.assert_called_with("/api/v2/custom_objects/car/access_rules/rule-1")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"access_rule": {"name": "R"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"access_rule": {}}
    client = AccessRuleApiClient(https)
    client.create("car", mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects/car/access_rules", json={"access_rule": {"name": "R"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"access_rule": {"name": "U"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"access_rule": {}}
    client = AccessRuleApiClient(https)
    client.update("car", "rule-1", mocker.Mock())
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/access_rules/rule-1", json={"access_rule": {"name": "U"}}
    )


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = AccessRuleApiClient(https)
    client.delete("car", "rule-1")
    https.delete.assert_called_with("/api/v2/custom_objects/car/access_rules/rule-1")


def test_definitions_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"definitions": {}}
    client = AccessRuleApiClient(https)
    client.definitions("car")
    https.get.assert_called_with("/api/v2/custom_objects/car/access_rules/definitions")


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
    client = AccessRuleApiClient(https)
    with pytest.raises(error_cls):
        client.get("car", "rule-1")


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
    client = AccessRuleApiClient(https)
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
    client = AccessRuleApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car", "rule-1")
