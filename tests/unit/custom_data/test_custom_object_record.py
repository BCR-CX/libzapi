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


MODULE = "libzapi.infrastructure.api_clients.custom_data.custom_object_record"


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"custom_object_record": {"name": "rec"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"custom_object_record": {}}
    client = CustomObjectRecordApiClient(https)
    client.create("car", mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects/car/records", json={"custom_object_record": {"name": "rec"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"custom_object_record": {"custom_object_fields": {}}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"custom_object_record": {}}
    client = CustomObjectRecordApiClient(https)
    client.update("car", "rec-1", mocker.Mock())
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/records/rec-1",
        json={"custom_object_record": {"custom_object_fields": {}}},
    )


def test_upsert_by_external_id(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"custom_object_record": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"custom_object_record": {}}
    client = CustomObjectRecordApiClient(https)
    client.upsert("car", mocker.Mock(), external_id="ext-1")
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/records?external_id=ext-1",
        json={"custom_object_record": {}},
    )


def test_upsert_by_name(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"custom_object_record": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.patch.return_value = {"custom_object_record": {}}
    client = CustomObjectRecordApiClient(https)
    client.upsert("car", mocker.Mock(), name="My Record")
    https.patch.assert_called_with(
        "/api/v2/custom_objects/car/records?name=My Record",
        json={"custom_object_record": {}},
    )


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = CustomObjectRecordApiClient(https)
    client.delete("car", "rec-1")
    https.delete.assert_called_with("/api/v2/custom_objects/car/records/rec-1")


def test_delete_by_external_id(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = CustomObjectRecordApiClient(https)
    client.delete_by_external_id("car", "ext-1")
    https.delete.assert_called_with("/api/v2/custom_objects/car/records?external_id=ext-1")


def test_delete_by_name(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = CustomObjectRecordApiClient(https)
    client.delete_by_name("car", "My Record")
    https.delete.assert_called_with("/api/v2/custom_objects/car/records?name=My Record")


def test_count_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"count": {"refreshed_at": "2024-01-01", "value": 42}}
    client = CustomObjectRecordApiClient(https)
    client.count("car")
    https.get.assert_called_with("/api/v2/custom_objects/car/records/count")


def test_search_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_records": [{}]}
    client = CustomObjectRecordApiClient(https)
    list(client.search("car", "query"))
    https.get.assert_called_with("/api/v2/custom_objects/car/records/search?query=query")


def test_search_with_sort(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_records": [{}]}
    client = CustomObjectRecordApiClient(https)
    list(client.search("car", "query", sort="-name"))
    https.get.assert_called_with("/api/v2/custom_objects/car/records/search?query=query&sort=-name")


def test_filtered_search_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_filtered_search", return_value={"filter": {"field": "value"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"custom_object_records": [{}]}
    client = CustomObjectRecordApiClient(https)
    list(client.filtered_search("car", mocker.Mock()))
    https.post.assert_called_with("/api/v2/custom_objects/car/records/search", json={"filter": {"field": "value"}})


def test_autocomplete_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_records": [{}]}
    client = CustomObjectRecordApiClient(https)
    list(client.autocomplete("car", "test"))
    https.get.assert_called_with("/api/v2/custom_objects/car/records/autocomplete?name=test")


def test_bulk_job_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_bulk_job", return_value={"job": {"action": "create", "items": []}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"job_status": {}}
    client = CustomObjectRecordApiClient(https)
    client.bulk_job("car", mocker.Mock())
    https.post.assert_called_with("/api/v2/custom_objects/car/jobs", json={"job": {"action": "create", "items": []}})


def test_incremental_export_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"custom_object_records": [{}], "end_of_stream": True}
    client = CustomObjectRecordApiClient(https)
    list(client.incremental_export("car", 1706820299))
    https.get.assert_called_with("/api/v2/incremental/custom_objects/car/cursor?start_time=1706820299")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.post.side_effect = error_cls("error")
    client = CustomObjectRecordApiClient(https)
    with pytest.raises(error_cls):
        client.create("car", mocker.Mock())


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
    client = CustomObjectRecordApiClient(https)
    with pytest.raises(error_cls):
        client.delete("car", "rec-1")
