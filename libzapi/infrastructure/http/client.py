import time
from http.client import RemoteDisconnected

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity

CONNECTION_MAX_AGE = 300  # 5 minutes


class HttpClient:
    def __init__(self, base_url: str, headers: dict[str, str], timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **headers,
        }
        self._retry = Retry(
            total=5,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            respect_retry_after_header=True,
        )
        self.timeout = timeout
        self._last_refresh = 0.0
        self.session = self._new_session()

    def _new_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(self._headers)
        adapter = HTTPAdapter(max_retries=self._retry)
        session.mount("https://", adapter)
        self._last_refresh = time.monotonic()
        return session

    def _refresh_if_stale(self) -> None:
        if time.monotonic() - self._last_refresh > CONNECTION_MAX_AGE:
            self.session.close()
            self.session = self._new_session()

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        self._refresh_if_stale()
        try:
            return self.session.request(method, f"{self.base_url}{path}", **kwargs)
        except (requests.ConnectionError, RemoteDisconnected):
            self.session.close()
            self.session = self._new_session()
            return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def _prepare_and_send(self, method: str, url: str, **kwargs) -> requests.Response:
        req = requests.Request(method, url, headers=self.session.headers)
        prepared = req.prepare()
        prepared.url = url  # override to prevent percent-encoding of brackets
        return self.session.send(prepared, **kwargs)

    def _request_raw(self, method: str, url: str, **kwargs) -> requests.Response:
        """Send a request with a pre-built URL, bypassing percent-encoding.

        Uses a manually prepared request so that literal characters like
        brackets in ``page[size]`` are preserved.
        """
        self._refresh_if_stale()
        try:
            return self._prepare_and_send(method, url, **kwargs)
        except (requests.ConnectionError, RemoteDisconnected):
            self.session.close()
            self.session = self._new_session()
            return self._prepare_and_send(method, url, **kwargs)

    def get(self, path: str, params: dict | None = None) -> dict:
        resp = self._request("GET", path, params=params, timeout=self.timeout)
        self._raise(resp)
        return resp.json()

    def get_raw(self, url: str) -> dict:
        """GET with a pre-built URL, bypassing query-param encoding.

        Some APIs (e.g. Sunshine Conversations) require literal brackets
        in query parameters like ``page[size]`` which ``requests``
        would otherwise percent-encode.
        """
        resp = self._request_raw("GET", url, timeout=self.timeout)
        self._raise(resp)
        return resp.json()

    def post(self, path: str, json: dict) -> dict:
        resp = self._request("POST", path, json=json, timeout=self.timeout)
        self._raise(resp)
        return resp.json()

    def put(self, path: str, json: dict) -> dict:
        resp = self._request("PUT", path, json=json, timeout=self.timeout)
        self._raise(resp)
        return resp.json()

    def patch(self, path: str, json: dict) -> dict:
        resp = self._request("PATCH", path, json=json, timeout=self.timeout)
        self._raise(resp)
        return resp.json()

    def post_multipart(self, path: str, files: dict, data: dict | None = None) -> dict:
        resp = self._request(
            "POST",
            path,
            files=files,
            data=data,
            headers={"Content-Type": None},
            timeout=self.timeout,
        )
        self._raise(resp)
        return resp.json()

    def delete(self, path: str) -> None:
        resp = self._request("DELETE", path, timeout=self.timeout)
        self._raise(resp)

    @staticmethod
    def _raise(resp: requests.Response) -> None:
        if resp.status_code == 401:
            raise Unauthorized(resp.text)
        if resp.status_code == 404:
            raise NotFound(resp.text)
        if resp.status_code == 422:
            raise UnprocessableEntity(resp.text)
        if resp.status_code == 429:
            raise RateLimited(resp.text)
        resp.raise_for_status()
