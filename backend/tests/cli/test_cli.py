"""Smoke tests for the beacon CLI.

Each test registers a stub response against an httpx.MockTransport and
invokes the CLI through Typer's CliRunner. No real backend is required.
"""

from __future__ import annotations

import json
from collections.abc import Callable

import httpx
import pytest
from typer.testing import CliRunner

from app import cli_client
from app.cli import app as cli_app


@pytest.fixture
def mock_transport(monkeypatch):
    """Patch BeaconClient to route every request through an in-memory transport."""
    handlers: list[tuple[Callable[[httpx.Request], bool], httpx.Response]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        for matches, response in handlers:
            if matches(request):
                return response
        return httpx.Response(500, json={"detail": "no matching stub"})

    transport = httpx.MockTransport(handler)
    original_init = cli_client.BeaconClient.__init__

    def patched_init(
        self,
        base_url: str,
        token: str | None = None,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        original_init(
            self,
            base_url=base_url,
            token=token,
            timeout=timeout,
            transport=transport,
        )

    def injecting_init(self, *args, **kwargs):
        kwargs.setdefault("transport", transport)
        patched_init(self, *args, **kwargs)

    monkeypatch.setattr(cli_client.BeaconClient, "__init__", injecting_init)

    def register(method: str, path: str, response: httpx.Response) -> None:
        handlers.append(
            (
                lambda r, m=method, p=path: r.method == m and r.url.path == p,
                response,
            )
        )

    return register


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _json_stdout(result) -> dict:
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_health_json(runner, mock_transport):
    mock_transport(
        "GET",
        "/health",
        httpx.Response(
            200, json={"status": "ok", "db": "connected", "version": "0.1.0"}
        ),
    )
    result = runner.invoke(cli_app, ["health", "--json"])
    assert result.exit_code == 0
    assert _json_stdout(result) == {
        "status": "ok",
        "db": "connected",
        "version": "0.1.0",
    }


def test_whoami_json(runner, mock_transport):
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "clerk_id": "user_abc",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "plan_tier": "free",
        "created_at": "2026-04-22T00:00:00Z",
    }
    mock_transport("GET", "/api/v1/me", httpx.Response(200, json=payload))
    result = runner.invoke(cli_app, ["whoami", "--json"])
    assert result.exit_code == 0
    assert _json_stdout(result)["email"] == "demo@example.com"


def test_whoami_auth_error(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/me",
        httpx.Response(401, json={"detail": "Invalid token"}),
    )
    result = runner.invoke(cli_app, ["whoami", "--json"])
    assert result.exit_code == 1
    body = _json_stdout(result)
    assert body == {"error": "Invalid token", "code": 1}


def test_search_json(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/search",
        httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "ein": "530196605",
                        "name": "American Red Cross",
                        "city": "Washington",
                        "state": "DC",
                        "ntee_code": "P20",
                        "latest_revenue": 3000000000,
                        "latest_expenses": 2800000000,
                        "latest_net_assets": 1000000000,
                        "latest_tax_year": 2023,
                    }
                ],
                "total": 1,
                "page": 1,
                "page_size": 20,
                "total_pages": 1,
            },
        ),
    )
    result = runner.invoke(
        cli_app, ["search", "food bank", "--state", "DC", "--json"]
    )
    assert result.exit_code == 0
    body = _json_stdout(result)
    assert body["total"] == 1
    assert body["items"][0]["ein"] == "530196605"


def test_typeahead_json(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/search/typeahead",
        httpx.Response(
            200,
            json=[
                {
                    "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                    "ein": "555555555",
                    "name": "Typeahead Test Org",
                    "city": "Columbus",
                    "state": "OH",
                }
            ],
        ),
    )
    result = runner.invoke(cli_app, ["typeahead", "type", "--json"])
    assert result.exit_code == 0
    body = json.loads(result.stdout.strip().splitlines()[-1])
    assert isinstance(body, list)
    assert body[0]["name"] == "Typeahead Test Org"


def test_org_ein_found(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/organizations/by-ein/310123456",
        httpx.Response(
            200,
            json={
                "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                "ein": "310123456",
                "name": "Buckeye Food Bank",
                "city": "Columbus",
                "state": "OH",
                "ntee_code": "K30",
                "ruling_date": None,
                "filings": [],
                "metrics": {
                    "program_expense_ratio": None,
                    "fundraising_efficiency": None,
                    "revenue_growth_rate": None,
                },
            },
        ),
    )
    result = runner.invoke(cli_app, ["org", "ein", "310123456", "--json"])
    assert result.exit_code == 0
    assert _json_stdout(result)["name"] == "Buckeye Food Bank"


def test_org_ein_not_found(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/organizations/by-ein/000000000",
        httpx.Response(404, json={"detail": "Organization not found"}),
    )
    result = runner.invoke(cli_app, ["org", "ein", "000000000", "--json"])
    assert result.exit_code == 2
    body = _json_stdout(result)
    assert body["code"] == 2
    assert "not found" in body["error"].lower()


def test_org_show_json(runner, mock_transport):
    org_id = "dddddddd-dddd-dddd-dddd-dddddddddddd"
    mock_transport(
        "GET",
        f"/api/v1/organizations/{org_id}",
        httpx.Response(
            200,
            json={
                "id": org_id,
                "ein": "310999999",
                "name": "Some Org",
                "city": None,
                "state": None,
                "ntee_code": None,
                "ruling_date": None,
                "filings": [],
                "metrics": {
                    "program_expense_ratio": None,
                    "fundraising_efficiency": None,
                    "revenue_growth_rate": None,
                },
            },
        ),
    )
    result = runner.invoke(cli_app, ["org", "show", org_id, "--json"])
    assert result.exit_code == 0
    assert _json_stdout(result)["id"] == org_id


def test_usage_json(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/usage/summary",
        httpx.Response(
            200,
            json={
                "searches_today": 3,
                "searches_this_month": 42,
                "profile_views_today": 1,
                "profile_views_this_month": 11,
            },
        ),
    )
    result = runner.invoke(cli_app, ["usage", "--json"])
    assert result.exit_code == 0
    assert _json_stdout(result)["searches_today"] == 3


def test_search_human_output(runner, mock_transport):
    mock_transport(
        "GET",
        "/api/v1/search",
        httpx.Response(
            200,
            json={
                "items": [],
                "total": 0,
                "page": 1,
                "page_size": 20,
                "total_pages": 0,
            },
        ),
    )
    result = runner.invoke(cli_app, ["search", "nothing"])
    assert result.exit_code == 0
    assert "0 result" in result.stdout
