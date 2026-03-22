import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.wfm.reports_service import ReportsService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return ReportsService(client), client


class TestGetData:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.get_data.return_value = [sentinel.row]
        result = service.get_data(template_id="t1", start_time=100, end_time=200)
        client.get_data.assert_called_once_with(template_id="t1", start_time=100, end_time=200)
        assert result == [sentinel.row]

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.get_data.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.get_data(template_id="t1", start_time=100, end_time=200)


class TestGetDataWithRelationships:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.get_data_with_relationships.return_value = {"data": []}
        result = service.get_data_with_relationships(template_id="t1", start_time=100, end_time=200)
        assert result == {"data": []}
