import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.category import Category
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import CategoryApiClient
from hypothesis import given

strategy = builds(
    Category,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Category) -> None:
    assert model.logical_key.as_str() == "category:cciia"


# ── API Client Tests ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key",
    [
        ("list_all", [], "/api/v2/help_center/categories", "categories"),
    ],
)
def test_category_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}

    client = CategoryApiClient(https)
    method = getattr(client, method_name)
    list(method(*args))

    https.get.assert_called_with(expected_path)


def test_category_api_client_get(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"category": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.category_api_client.to_domain",
        return_value=mocker.Mock(),
    )

    client = CategoryApiClient(https)
    client.get(fake_id)

    https.get.assert_called_with(f"/api/v2/help_center/categories/{fake_id}")


def test_category_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"category": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.category_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.category_api_client.to_payload_create",
        return_value={"category": {"name": "test"}},
    )

    client = CategoryApiClient(https)
    cmd = mocker.Mock()
    client.create(cmd)

    https.post.assert_called_with(
        "/api/v2/help_center/categories",
        json={"category": {"name": "test"}},
    )


def test_category_api_client_update(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"category": {}}

    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.category_api_client.to_domain",
        return_value=mocker.Mock(),
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.category_api_client.to_payload_update",
        return_value={"category": {"name": "updated"}},
    )

    client = CategoryApiClient(https)
    cmd = mocker.Mock()
    client.update(fake_id, cmd)

    https.put.assert_called_with(
        f"/api/v2/help_center/categories/{fake_id}",
        json={"category": {"name": "updated"}},
    )


def test_category_api_client_delete(mocker):
    fake_id = 12345
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"

    client = CategoryApiClient(https)
    client.delete(fake_id)

    https.delete.assert_called_with(f"/api/v2/help_center/categories/{fake_id}")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_category_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CategoryApiClient(https)

    with pytest.raises(error_cls):
        client.get(1)
