import libzapi.infrastructure.api_clients.voice as api
from libzapi.application.services.voice.addresses_service import AddressesService
from libzapi.application.services.voice.availabilities_service import AvailabilitiesService
from libzapi.application.services.voice.callback_requests_service import CallbackRequestsService
from libzapi.application.services.voice.digital_lines_service import DigitalLinesService
from libzapi.application.services.voice.greetings_service import GreetingsService
from libzapi.application.services.voice.incremental_exports_service import IncrementalExportsService
from libzapi.application.services.voice.ivr_menus_service import IvrMenusService
from libzapi.application.services.voice.ivr_routes_service import IvrRoutesService
from libzapi.application.services.voice.ivrs_service import IvrsService
from libzapi.application.services.voice.lines_service import LinesService
from libzapi.application.services.voice.phone_numbers_service import PhoneNumbersService
from libzapi.application.services.voice.recordings_service import RecordingsService
from libzapi.application.services.voice.stats_service import StatsService
from libzapi.application.services.voice.voice_settings_service import VoiceSettingsService
from libzapi.infrastructure.http.auth import api_token_headers, oauth_headers
from libzapi.infrastructure.http.client import HttpClient


class Voice:
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

        # Initialize services
        self.phone_numbers = PhoneNumbersService(api.PhoneNumberApiClient(http))
        self.digital_lines = DigitalLinesService(api.DigitalLineApiClient(http))
        self.lines = LinesService(api.LineApiClient(http))
        self.availabilities = AvailabilitiesService(api.AvailabilityApiClient(http))
        self.greetings = GreetingsService(api.GreetingApiClient(http))
        self.callback_requests = CallbackRequestsService(api.CallbackRequestApiClient(http))
        self.stats = StatsService(api.StatsApiClient(http))
        self.incremental_exports = IncrementalExportsService(api.IncrementalExportApiClient(http))
        self.recordings = RecordingsService(api.RecordingApiClient(http))
        self.addresses = AddressesService(api.AddressApiClient(http))
        self.voice_settings = VoiceSettingsService(api.VoiceSettingsApiClient(http))
        self.ivrs = IvrsService(api.IvrApiClient(http))
        self.ivr_menus = IvrMenusService(api.IvrMenuApiClient(http))
        self.ivr_routes = IvrRoutesService(api.IvrRouteApiClient(http))
