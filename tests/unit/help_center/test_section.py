import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.section import Section
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import SectionApiClient
from hypothesis import given

strategy = builds(
    Section,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Section):
    assert model.logical_key.as_str() == "section:cciia"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/sections", "sections"),
    ],
)
def test_section_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = SectionApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_section_api_client_get(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"section": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.section_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = SectionApiClient(https)
    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/help_center/sections/{fake_id}")


def test_section_api_client_create(mocker):
    fake_category_id = 999
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"section": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.section_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.section_api_client.to_payload_create",
        return_value={"section": {"name": "test"}},
    )

    client = SectionApiClient(https)
    cmd = mocker.Mock()
    client.create(fake_category_id, cmd)

    https.post.assert_called_with(
        f"/api/v2/help_center/categories/{fake_category_id}/sections",
        json={"section": {"name": "test"}},
    )


def test_section_api_client_update(mocker):
    fake_id = 12345
    locale = "en-us"
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"section": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.section_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.section_api_client.to_payload_update",
        return_value={"section": {"name": "updated"}},
    )

    client = SectionApiClient(https)
    cmd = mocker.Mock()
    client.update(fake_id, locale, cmd)

    https.put.assert_called_with(
        f"/api/v2/help_center/{locale}/sections/{fake_id}",
        json={"section": {"name": "updated"}},
    )


def test_section_api_client_delete(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = SectionApiClient(https)
    client.delete(fake_id)

    https.delete.assert_called_with(f"/api/v2/help_center/sections/{fake_id}")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_section_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = SectionApiClient(https)

    with pytest.raises(error_cls):
        client.get(1)
