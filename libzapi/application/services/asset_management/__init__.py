from libzapi.application.services.asset_management.assets_service import AssetsService
from libzapi.application.services.asset_management.asset_types_service import AssetTypesService
from libzapi.application.services.asset_management.asset_fields_service import AssetFieldsService
from libzapi.application.services.asset_management.asset_locations_service import AssetLocationsService
from libzapi.application.services.asset_management.asset_statuses_service import AssetStatusesService
from libzapi.infrastructure.http.auth import oauth_headers, api_token_headers
from libzapi.infrastructure.http.client import HttpClient
import libzapi.infrastructure.api_clients.asset_management as api


class AssetManagement:
    def __init__(
        self, base_url: str, oauth_token: str | None = None, email: str | None = None, api_token: str | None = None
    ):
        if oauth_token:
            headers = oauth_headers(oauth_token)
        elif email and api_token:
            headers = api_token_headers(email, api_token)
        else:
            raise ValueError("Provide oauth_token or email+api_token")

        http = HttpClient(base_url, headers=headers)

        self.assets = AssetsService(api.AssetApiClient(http))
        self.asset_types = AssetTypesService(api.AssetTypeApiClient(http))
        self.asset_fields = AssetFieldsService(api.AssetFieldApiClient(http))
        self.asset_locations = AssetLocationsService(api.AssetLocationApiClient(http))
        self.asset_statuses = AssetStatusesService(api.AssetStatusApiClient(http))
