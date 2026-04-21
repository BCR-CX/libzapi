from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.domain.models.ticketing.attachment import Attachment
from libzapi.domain.models.ticketing.upload import Upload


attachment_strategy = builds(Attachment, file_name=just("f.png"))
upload_strategy = builds(
    Upload,
    token=just("abc-token"),
    attachment=attachment_strategy,
    attachments=just([]),
)


@given(upload_strategy)
def test_upload_logical_key_uses_token(upload: Upload) -> None:
    assert upload.logical_key.as_str() == "upload:abc-token"
