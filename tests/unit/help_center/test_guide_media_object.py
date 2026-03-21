import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.guide_media_object import Media
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import GuideMediaApiClient
from hypothesis import given

strategy = builds(
    Media,
    name=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: Media):
    assert model.logical_key.as_str() == "guide_media_object:cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key", [("list_all", [], "/api/v2/guide/medias", "guide_medias")]
)
def test_guide_media_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = GuideMediaApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_guide_media_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"guide_media": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.guide_media_api_client.to_domain", return_value=mocker.Mock()
    )
    client = GuideMediaApiClient(https)
    client.get(12345)
    https.get.assert_called_with("/api/v2/guide/medias/12345")


def test_guide_media_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post_multipart.return_value = {"guide_media": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.guide_media_api_client.to_domain", return_value=mocker.Mock()
    )
    client = GuideMediaApiClient(https)
    client.create(file=("test.png", b"data", "image/png"))
    https.post_multipart.assert_called_with("/api/v2/guide/medias", files={"file": ("test.png", b"data", "image/png")})


def test_guide_media_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = GuideMediaApiClient(https)
    client.delete(12345)
    https.delete.assert_called_with("/api/v2/guide/medias/12345")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_guide_media_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = GuideMediaApiClient(https)
    with pytest.raises(error_cls):
        client.get(1)
