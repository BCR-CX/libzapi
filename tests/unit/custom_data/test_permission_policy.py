import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.custom_data.permission_policy import PermissionPolicy
from libzapi.infrastructure.api_clients.custom_data.permission_policy import PermissionPolicyApiClient

MODULE = "libzapi.infrastructure.api_clients.custom_data.permission_policy"

strategy = builds(PermissionPolicy, id=just("policy-1"))


@given(strategy)
def test_logical_key(model: PermissionPolicy):
    assert model.logical_key.as_str() == "permission_policy:policy-1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"permission_policies": [{}]}
    client = PermissionPolicyApiClient(https)
    list(client.list_all("car"))
    https.get.assert_called_with("/api/v2/custom_objects/car/permission_policies")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"permission_policy": {}}
    client = PermissionPolicyApiClient(https)
    client.get("car", "custom-role-123")
    https.get.assert_called_with("/api/v2/custom_objects/car/permission_policies/custom-role-123")


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"permission_policy": {"read": "all"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"permission_policy": {}}
    client = PermissionPolicyApiClient(https)
    client.update("car", "custom-role-123", mocker.Mock())
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/permission_policies/custom-role-123",
        json={"permission_policy": {"read": "all"}},
    )


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
    client = PermissionPolicyApiClient(https)
    with pytest.raises(error_cls):
        client.get("car", "p-1")
