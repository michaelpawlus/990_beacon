"""HTTP client for the 990 Beacon CLI.

Wraps httpx.Client with typed exceptions so commands can translate failures
into the exit codes the CLI spec requires (0 success, 1 error, 2 not found).
"""

from __future__ import annotations

from typing import Any

import httpx


class BeaconError(Exception):
    """Base class for beacon CLI HTTP errors."""


class BeaconNetworkError(BeaconError):
    """Transport-level failure (DNS, connect, timeout, TLS)."""


class BeaconAuthError(BeaconError):
    """HTTP 401/403 from the backend."""


class BeaconNotFoundError(BeaconError):
    """HTTP 404 from the backend."""


class BeaconClient:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        headers: dict[str, str] = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> BeaconClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        try:
            response = self._client.get(path, params=clean or None)
        except httpx.HTTPError as exc:
            raise BeaconNetworkError(str(exc)) from exc
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: httpx.Response) -> Any:
        if response.status_code in (401, 403):
            raise BeaconAuthError(_detail(response) or "unauthorized")
        if response.status_code == 404:
            raise BeaconNotFoundError(_detail(response) or "not found")
        if response.status_code >= 400:
            raise BeaconError(
                _detail(response) or f"HTTP {response.status_code}"
            )
        try:
            return response.json()
        except ValueError as exc:
            raise BeaconError(f"invalid JSON response: {exc}") from exc


def _detail(response: httpx.Response) -> str | None:
    try:
        data = response.json()
    except ValueError:
        return None
    if isinstance(data, dict):
        value = data.get("detail") or data.get("error")
        return str(value) if value else None
    return None
