import pytest

from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.user_segment import UserSegment
from libzapi.application.commands.help_center.user_segments_cmds import CreateUserSegmentCmd, UserType
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import UserSegmentApiClient
from hypothesis import given

strategy = builds(
    UserSegment,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: UserSegment) -> None:
    assert model.logical_key.as_str() == "user_segment:cciia"


def test_create_user_segment_command_fail():
    with pytest.raises(ValueError):
        CreateUserSegmentCmd(
            name="Test Segment",
            user_type=UserType("no-user-allowed"),  # Invalid user_type
        )


def test_create_user_segment_command_success():
    cmd = CreateUserSegmentCmd(name="Test Segment", user_type=UserType("signed_in_users"))
    assert cmd.name == "Test Segment"
    assert cmd.user_type.value == "signed_in_users"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/user_segments", "user_segments"),
        ("list_applicable", [], "/api/v2/help_center/user_segments/applicable", "user_segments"),
        ("list_user", [789], "/api/v2/help_center/users/789/user_segments", "user_segments"),
        ("list_sections", [456], "/api/v2/help_center/user_segments/456/sections", "sections"),
        ("list_topics", [456], "/api/v2/help_center/user_segments/456/topics", "topics"),
    ],
)
def test_user_segment_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = UserSegmentApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_user_segment_api_client_get(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"user_segment": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.user_segment_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = UserSegmentApiClient(https)
    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/help_center/user_segments/{fake_id}")


def test_user_segment_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"user_segment": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.user_segment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.user_segment_api_client.to_payload_create",
        return_value={"user_segment": {"name": "test"}},
    )

    client = UserSegmentApiClient(https)
    cmd = mocker.Mock()
    client.create(cmd)

    https.post.assert_called_with(
        "/api/v2/help_center/user_segments",
        json={"user_segment": {"name": "test"}},
    )


def test_user_segment_api_client_update(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"user_segment": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.user_segment_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.user_segment_api_client.to_payload_update",
        return_value={"user_segment": {"name": "updated"}},
    )

    client = UserSegmentApiClient(https)
    cmd = mocker.Mock()
    client.update(fake_id, cmd)

    https.put.assert_called_with(
        f"/api/v2/help_center/user_segments/{fake_id}",
        json={"user_segment": {"name": "updated"}},
    )


def test_user_segment_api_client_delete(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = UserSegmentApiClient(https)
    client.delete(fake_id)

    https.delete.assert_called_with(f"/api/v2/help_center/user_segments/{fake_id}")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_user_segment_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = UserSegmentApiClient(https)

    with pytest.raises(error_cls):
        client.get(1)
