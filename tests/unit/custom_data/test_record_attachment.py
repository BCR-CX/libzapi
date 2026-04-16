import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.custom_data.record_attachment import RecordAttachment
from libzapi.infrastructure.api_clients.custom_data.record_attachment import RecordAttachmentApiClient

MODULE = "libzapi.infrastructure.api_clients.custom_data.record_attachment"

strategy = builds(RecordAttachment, id=just("att-1"))


@given(strategy)
def test_logical_key(model: RecordAttachment):
    assert model.logical_key.as_str() == "record_attachment:att-1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"attachments": [{}]}
    client = RecordAttachmentApiClient(https)
    list(client.list_all("car", "rec-1"))
    https.get.assert_called_with("/api/v2/custom_objects/car/records/rec-1/attachments")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post_multipart.return_value = {"attachment": {}}
    client = RecordAttachmentApiClient(https)
    client.create("car", "rec-1", ("file.txt", b"data", "text/plain"))
    https.post_multipart.assert_called_with(
        "/api/v2/custom_objects/car/records/rec-1/attachments",
        files={"file": ("file.txt", b"data", "text/plain")},
    )


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = RecordAttachmentApiClient(https)
    client.delete("car", "rec-1", "att-1")
    https.delete.assert_called_with("/api/v2/custom_objects/car/records/rec-1/attachments/att-1")


def test_download_url(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = RecordAttachmentApiClient(https)
    url = client.download_url("car", "rec-1", "att-1")
    assert url == "https://example.zendesk.com/api/v2/custom_objects/car/records/rec-1/attachments/att-1/download"


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = RecordAttachmentApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_all("car", "rec-1"))


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
    client = RecordAttachmentApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car", "rec-1", "att-1")
