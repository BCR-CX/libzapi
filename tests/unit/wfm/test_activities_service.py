import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.services.wfm.activities_service import ActivitiesService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity


def _make_service(client=None):
    client = client or Mock()
    return ActivitiesService(client), client


class TestList:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.list.return_value = [sentinel.activity]
        result = service.list(start_time=100)
        client.list.assert_called_once_with(start_time=100)
        assert result == [sentinel.activity]

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list(start_time=100)


class TestListWithRelationships:
    def test_delegates_to_client(self):
        service, client = _make_service()
        client.list_with_relationships.return_value = ([], [], [])
        result = service.list_with_relationships(start_time=100)
        client.list_with_relationships.assert_called_once_with(start_time=100)
        assert result == ([], [], [])
