import pytest
from hypothesis import given
from hypothesis.strategies import builds

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.stats import AccountOverview
from libzapi.infrastructure.api_clients.voice.stats_api_client import StatsApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.stats_api_client"

strategy = builds(AccountOverview)


@given(strategy)
def test_logical_key(model: AccountOverview) -> None:
    assert model.logical_key.as_str() == "account_overview:current"


def test_account_overview_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"account_overview": {}}
    client = StatsApiClient(https)
    client.account_overview()
    https.get.assert_called_with("/api/v2/channels/voice/stats/account_overview")


def test_account_overview_with_phone_number_ids(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"account_overview": {}}
    client = StatsApiClient(https)
    client.account_overview(phone_number_ids=[1, 2])
    https.get.assert_called_with("/api/v2/channels/voice/stats/account_overview?phone_number_ids=1,2")


def test_agents_activity_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"agents_activity": []}
    client = StatsApiClient(https)
    client.agents_activity()
    https.get.assert_called_with("/api/v2/channels/voice/stats/agents_activity")


def test_agents_overview_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"agents_overview": {}}
    client = StatsApiClient(https)
    client.agents_overview()
    https.get.assert_called_with("/api/v2/channels/voice/stats/agents_overview")


def test_current_queue_activity_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"current_queue_activity": {}}
    client = StatsApiClient(https)
    client.current_queue_activity()
    https.get.assert_called_with("/api/v2/channels/voice/stats/current_queue_activity")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_account_overview_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = StatsApiClient(https)
    with pytest.raises(error_cls):
        client.account_overview()
