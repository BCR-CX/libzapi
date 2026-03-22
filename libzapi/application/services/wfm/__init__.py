import libzapi.infrastructure.api_clients.wfm as api
from libzapi.application.services.wfm.activities_service import ActivitiesService
from libzapi.application.services.wfm.reports_service import ReportsService
from libzapi.application.services.wfm.shifts_service import ShiftsService
from libzapi.application.services.wfm.teams_service import TeamsService
from libzapi.application.services.wfm.time_off_service import TimeOffService
from libzapi.infrastructure.http.auth import api_token_headers, oauth_headers
from libzapi.infrastructure.http.client import HttpClient


class WorkforceManagement:
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

        self.activities = ActivitiesService(api.ActivityApiClient(http))
        self.reports = ReportsService(api.ReportApiClient(http))
        self.shifts = ShiftsService(api.ShiftApiClient(http))
        self.time_off = TimeOffService(api.TimeOffApiClient(http))
        self.teams = TeamsService(api.TeamApiClient(http))
