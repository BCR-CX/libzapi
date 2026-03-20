import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.custom_data.custom_object_record import (
    CustomObjectRecordApiClient,
    build_query,
)


# ── build_query ──────────────────────────────────────────────────────────


def test_build_query_with_all_params():
    result = build_query(
        external_ids=["ext1", "ext2"],
        ids=["id1", "id2"],
        page_size=50,
        sort_type="id",
        sort_order="asc",
    )
    assert "filter[external_ids]=ext1,ext2" in result
    assert "filter[ids]=id1,id2" in result
    assert "page[size]=50" in result
    assert "sort=id" in result


def test_build_query_desc_sort_order():
    result = build_query(
        external_ids=[],
        ids=[],
        page_size=10,
        sort_type="updated_at",
        sort_order="desc",
    )
    assert "sort=-updated_at" in result


def test_build_query_asc_sort_order():
    result = build_query(
        external_ids=[],
        ids=[],
        page_size=10,
        sort_type="id",
        sort_order="asc",
    )
    assert "sort=id" in result


def test_build_query_no_optional_filters():
    result = build_query(
        external_ids=[],
        ids=[],
        page_size=0,
        sort_type="id",
        sort_order="asc",
    )
    assert "filter[external_ids]" not in result
    assert "filter[ids]" not in result
    assert "page[size]" not in result


def test_build_query_invalid_sort_type():
    with pytest.raises(ValueError, match="Invalid sort_type"):
        build_query(
            external_ids=[],
            ids=[],
            page_size=10,
            sort_type="invalid",
            sort_order="asc",
        )


def test_build_query_invalid_sort_order():
    with pytest.raises(ValueError, match="Invalid sort_order"):
        build_query(
            external_ids=[],
            ids=[],
            page_size=10,
            sort_type="id",
            sort_order="invalid",
        )


# ── list_all ─────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object_record.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_records": [{}]}

    client = CustomObjectRecordApiClient(https)
    list(
        client.list_all(
            custom_object_key="car",
            external_ids=[],
            ids=[],
            page_size=10,
            sort_type="id",
            sort_order="asc",
        )
    )

    expected_query = build_query(external_ids=[], ids=[], page_size=10, sort_type="id", sort_order="asc")
    https.get.assert_called_with(f"/api/v2/custom_objects/car/records?{expected_query}")


# ── get ──────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object_record.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_record": {"id": "rec-1"}}

    client = CustomObjectRecordApiClient(https)
    client.get("car", "rec-1")

    https.get.assert_called_with("/api/v2/custom_objects/car/records/rec-1")
    mock_to_domain.assert_called_once()


# ── limit ────────────────────────────────────────────────────────────────


def test_limit_calls_correct_path(mocker):
    mock_to_domain = mocker.patch(
        "libzapi.infrastructure.api_clients.custom_data.custom_object_record.to_domain",
        return_value=mocker.Mock(),
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"count": 10, "limit": 100000}

    client = CustomObjectRecordApiClient(https)
    client.limit()

    https.get.assert_called_with("/api/v2/custom_objects/limits/record_limit")
    mock_to_domain.assert_called_once()


# ── error propagation ───────────────────────────────────────────────────


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
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectRecordApiClient(https)

    with pytest.raises(error_cls):
        list(
            client.list_all(
                custom_object_key="car",
                external_ids=[],
                ids=[],
                page_size=10,
                sort_type="id",
                sort_order="asc",
            )
        )


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectRecordApiClient(https)

    with pytest.raises(error_cls):
        client.get("car", "rec-1")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_limit_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = CustomObjectRecordApiClient(https)

    with pytest.raises(error_cls):
        client.limit()
