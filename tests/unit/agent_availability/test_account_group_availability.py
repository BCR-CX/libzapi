import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.agent_availability.account_group_availability_api_client import (
    AccountGroupAvailabilityApiClient,
)


MODULE = "libzapi.infrastructure.api_clients.agent_availability.account_group_availability_api_client"
BASE = "/api/v2/account_groups/availability"


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"account_id": 1, "group_id": 10}

    client = AccountGroupAvailabilityApiClient(https)
    client.get(10)

    https.get.assert_called_with(f"{BASE}/10")


# ── error propagation ──────────────────────────────────────────────────


ERROR_CLASSES = [
    pytest.param(Unauthorized, id="401"),
    pytest.param(NotFound, id="404"),
    pytest.param(UnprocessableEntity, id="422"),
    pytest.param(RateLimited, id="429"),
]


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = AccountGroupAvailabilityApiClient(https)

    with pytest.raises(error_cls):
        client.get(10)
