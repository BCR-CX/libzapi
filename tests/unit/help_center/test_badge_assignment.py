import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.badge_assignment import BadgeAssignment
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import BadgeAssignmentApiClient
from hypothesis import given

strategy = builds(
    BadgeAssignment,
    id=just("234"),
)


@given(strategy)
def test_session_logical_key_from_id(model: BadgeAssignment):
    assert model.logical_key.as_str() == "badge_assignment:id_234"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [("list_all", [], "/api/v2/gather/badge_assignments", "badge_assignments")],
)
def test_badge_assignment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = BadgeAssignmentApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_badge_assignment_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"badge_assignment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_assignment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    client = BadgeAssignmentApiClient(https)
    client.get("abc123")
    https.get.assert_called_with("/api/v2/gather/badge_assignments/abc123")


def test_badge_assignment_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"badge_assignment": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_assignment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.badge_assignment_api_client.to_payload_create",
        return_value={"badge_assignment": {"badge_id": "b1"}},
    )
    client = BadgeAssignmentApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/gather/badge_assignments", json={"badge_assignment": {"badge_id": "b1"}})


def test_badge_assignment_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = BadgeAssignmentApiClient(https)
    client.delete("abc123")
    https.delete.assert_called_with("/api/v2/gather/badge_assignments/abc123")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_badge_assignment_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = BadgeAssignmentApiClient(https)
    with pytest.raises(error_cls):
        client.get("1")
