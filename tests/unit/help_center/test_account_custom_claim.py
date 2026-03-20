import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.account_custom_claim import CustomClaim
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import AccountCustomClaimApiClient
from hypothesis import given

strategy = builds(
    CustomClaim,
    claim_identifier=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: CustomClaim):
    assert model.logical_key.as_str() == "custom_claim:cciia"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/integration/account_custom_claims", "custom_claims"),
    ],
)
def test_account_custom_claim_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = AccountCustomClaimApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_account_custom_claim_api_client_get(mocker):
    fake_id = "claim_123"
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_claim": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.account_custom_claim_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = AccountCustomClaimApiClient(https)
    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/help_center/integration/account_custom_claims/{fake_id}")


def test_account_custom_claim_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"custom_claim": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.account_custom_claim_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.account_custom_claim_api_client.to_payload_create",
        return_value={"custom_claim": {"name": "test"}},
    )

    client = AccountCustomClaimApiClient(https)
    cmd = mocker.Mock()
    client.create(cmd)

    https.post.assert_called_with(
        "/api/v2/help_center/integration/account_custom_claims",
        json={"custom_claim": {"name": "test"}},
    )


def test_account_custom_claim_api_client_update(mocker):
    fake_id = "claim_123"
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"custom_claim": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.account_custom_claim_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.account_custom_claim_api_client.to_payload_update",
        return_value={"custom_claim": {"name": "updated"}},
    )

    client = AccountCustomClaimApiClient(https)
    cmd = mocker.Mock()
    client.update(fake_id, cmd)

    https.put.assert_called_with(
        f"/api/v2/help_center/integration/account_custom_claims/{fake_id}",
        json={"custom_claim": {"name": "updated"}},
    )


def test_account_custom_claim_api_client_delete(mocker):
    fake_id = "claim_123"
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = AccountCustomClaimApiClient(https)
    client.delete(fake_id)

    https.delete.assert_called_with(f"/api/v2/help_center/integration/account_custom_claims/{fake_id}")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_account_custom_claim_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AccountCustomClaimApiClient(https)

    with pytest.raises(error_cls):
        client.get("claim_1")
