import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.brand import Brand
from libzapi.infrastructure.api_clients.ticketing import BrandApiClient


strategy = builds(
    Brand,
    name=just("ACME"),
)


@given(strategy)
def test_brand_logical_key_from_name(model: Brand):
    assert model.logical_key.as_str() == "brand:acme"


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.brand_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# list / get
# ---------------------------------------------------------------------------


def test_list_endpoint(http, domain):
    http.get.return_value = {"brands": []}
    client = BrandApiClient(http)
    list(client.list())
    http.get.assert_called_with("/api/v2/brands")


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "brands": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = BrandApiClient(http)
    assert len(list(client.list())) == 2


def test_get_endpoint(http, domain):
    http.get.return_value = {"brand": {"id": 5}}
    client = BrandApiClient(http)
    client.get(brand_id=5)
    http.get.assert_called_with("/api/v2/brands/5")


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"brand": {"id": 1}}
    client = BrandApiClient(http)
    client.create(CreateBrandCmd(name="Acme", subdomain="acme"))
    http.post.assert_called_with(
        "/api/v2/brands", {"brand": {"name": "Acme", "subdomain": "acme"}}
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"brand": {"id": 1}}
    client = BrandApiClient(http)
    client.update(brand_id=5, entity=UpdateBrandCmd(signature_template="sig"))
    http.put.assert_called_with(
        "/api/v2/brands/5", {"brand": {"signature_template": "sig"}}
    )


def test_delete_calls_endpoint(http):
    client = BrandApiClient(http)
    client.delete(brand_id=9)
    http.delete.assert_called_with("/api/v2/brands/9")


# ---------------------------------------------------------------------------
# check_host_mapping
# ---------------------------------------------------------------------------


def test_check_host_mapping_calls_endpoint(http):
    http.get.return_value = {"ok": True}
    client = BrandApiClient(http)
    result = client.check_host_mapping(host_mapping="help.x.com", subdomain="x")
    http.get.assert_called_with(
        "/api/v2/brands/check_host_mapping?host_mapping=help.x.com&subdomain=x"
    )
    assert result == {"ok": True}


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = BrandApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())
